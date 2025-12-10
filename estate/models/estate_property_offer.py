# estate/models/estate_property_offer.py

from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import timedelta

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real Estate Property Offer'
    _order = "price desc"

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
    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            # Note: create_date is implicitly False if the record is brand new (before creation)
            if record.create_date:
                # deadline = create_date + validity days
                record.date_deadline = fields.Date.to_date(record.create_date) + timedelta(
                    days=record.validity
                )
            else:
                # If no creation date (e.g., brand new record in UI), set a default based on today
                record.date_deadline = fields.Date.today() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline and record.create_date:
                # validity = deadline_date - create_date (as days)
                record.validity = (record.date_deadline - fields.Date.to_date(record.create_date)).days
            # We don't need an else, as the validity field will retain its value or default

    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True, string="Deadline")

    # --- CORRECTED CREATE METHOD ---
    @api.model
    def create(self, vals_list):
        """
        Custom create method to prevent creating offers on sold/canceled properties.
        Also updates property state to 'offer_received'.
        """
        # The ORM passes a list of dictionaries (vals_list)
        for vals in vals_list:
            property_id = vals.get('property_id')
            
            if property_id:
                # Check the property state before creating the offer
                property_record = self.env['estate.property'].browse(property_id)
                
                # Constraint check: Cannot create offer on a sold or canceled property
                if property_record.state in ('sold', 'canceled'):
                    raise UserError("You cannot create an offer for a property that is already sold or canceled.")
                
                # Change property state to 'offer_received'
                # Only if the property is 'new' (not already offer_received)
                if property_record.state == 'new':
                    property_record.state = 'offer_received'

        # Call the original create method
        return super(EstatePropertyOffer, self).create(vals_list)


    # Workflow Methods
    def action_accept(self):
        """Accepts the current offer, updates the property, and refuses all others."""
        for record in self:
            # Check for sale/cancel status *before* updating the offer
            if record.property_id.state in ['sold', 'canceled']:
                raise UserError("Cannot accept an offer for a property that is sold or canceled.")
            
            # Refuse all other existing offers for this property
            other_offers = record.property_id.offer_ids.filtered(lambda r: r.id != record.id and r.status != 'refused')
            other_offers.action_refuse()
            
            record.status = 'accepted'
            
            # Update parent property with selling details and state
            record.property_id.write({
                'selling_price': record.price,
                'buyer_id': record.partner_id.id,
                'state': 'offer_accepted',
            })

        return True

    def action_refuse(self):
        """Refuses the current offer and potentially resets the property state."""
        for record in self:
            # Check if the offer is already refused to avoid unnecessary state changes
            if record.status != 'refused':
                record.status = 'refused'
                
                # Check if this property has any remaining accepted offers
                remaining_accepted = record.property_id.offer_ids.filtered(lambda r: r.status == 'accepted')
                
                if not remaining_accepted:
                    # If no accepted offers remain, reset property selling details
                    # If there are *any* offers (even refused ones), state is 'offer_received', otherwise 'new'.
                    new_state = 'offer_received' if record.property_id.offer_ids else 'new'
                    
                    record.property_id.write({
                        'selling_price': 0.0,
                        'buyer_id': False,
                        'state': new_state,
                    })
        return True