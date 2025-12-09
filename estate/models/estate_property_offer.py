from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import timedelta

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real Estate Property Offer'
    _order = "price desc" # Offers should be ordered by price descending

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ],
        copy=False
    )
    partner_id = fields.Many2one('res.partner', required=True, string="Partner")
    property_id = fields.Many2one('estate.property', required=True, string="Property")
    validity = fields.Integer(default=7, string="Validity (days)")
    
    # Computed/Inverse Field for Date Deadline
    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                # deadline = create_date + validity days
                record.date_deadline = fields.Date.to_date(record.create_date) + timedelta(
                    days=record.validity
                )
            else:
                # If no creation date (e.g., brand new record), set a default
                record.date_deadline = fields.Date.today() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline and record.create_date:
                # validity = deadline_date - create_date (as days)
                record.validity = (record.date_deadline - fields.Date.to_date(record.create_date)).days

    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True, string="Deadline")

    # Workflow Methods
    def action_accept(self):
        """Accepts the current offer, updates the property, and refuses all others."""
        for record in self:
            if record.property_id.state in ['sold', 'canceled']:
                raise UserError("Cannot accept an offer for a property that is sold or canceled.")
            
            # Refuse all existing accepted offers (only one accepted offer allowed)
            accepted_offers = record.property_id.offer_ids.filtered(lambda r: r.status == 'accepted')
            if accepted_offers:
                raise UserError("An offer has already been accepted for this property. Please refuse the existing accepted offer first.")
                
            record.status = 'accepted'
            
            # Update parent property
            record.property_id.write({
                'selling_price': record.price,
                'buyer_id': record.partner_id.id,
                'state': 'offer_accepted',
            })
            
            # Refuse all other offers for this property
            other_offers = record.property_id.offer_ids.filtered(lambda r: r.id != record.id)
            other_offers.action_refuse()

        return True

    def action_refuse(self):
        """Refuses the current offer and potentially resets the property state."""
        for record in self:
            record.status = 'refused'
            
            # If the refused offer was the one accepted, reset the property's accepted status
            if record.property_id.selling_price == record.price and record.property_id.state == 'offer_accepted':
                # Check if there are any other accepted offers
                remaining_accepted = record.property_id.offer_ids.filtered(lambda r: r.status == 'accepted')
                
                # If no accepted offers remain, reset property details
                if not remaining_accepted:
                    record.property_id.write({
                        'selling_price': 0.0,
                        'buyer_id': False,
                        # If there are still other offers, set to 'offer_received', otherwise 'new'
                        'state': 'offer_received' if record.property_id.offer_ids else 'new',
                    })
        return True