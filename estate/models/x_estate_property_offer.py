# estate/models/x_estate_property_offer.py

from odoo import models, fields, api
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = 'x_estate.property.offer'
    _description = 'Real Estate Property Offer'
    _order = "x_price desc"
    
    # Required Fields
    x_price = fields.Float(required=True, string="Price")
    x_status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        copy=False,
        string="Status"
    )
    
    # Relationships 
    x_partner_id = fields.Many2one('res.partner', required=True, string="Partner")
    # Many2one link back to the parent property (estate.property)
    x_property_id = fields.Many2one('estate.property', required=True, string="Property")
    
    # Optional: Add validity and deadline fields if needed
    x_validity = fields.Integer(default=7, string="Validity (days)")
    x_date_deadline = fields.Date(string="Deadline")
    
    # --- CREATE METHOD ---
    @api.model
    def create(self, vals_list):
        """
        Custom create method to prevent creating offers on sold/canceled properties.
        Also updates property state to 'offer_received'.
        """
        for vals in vals_list:
            property_id = vals.get('x_property_id')
            
            if property_id:
                # Check the property state before creating the offer
                property_record = self.env['estate.property'].browse(property_id)
                
                # Constraint check: Cannot create offer on a sold or canceled property
                if property_record.state in ('sold', 'canceled'):
                    raise UserError("You cannot create an offer for a property that is already sold or canceled.")
                
                # Change property state to 'offer_received'
                if property_record.state == 'new':
                    property_record.state = 'offer_received'

        # Call the original create method
        return super(EstatePropertyOffer, self).create(vals_list)
    
    # --- ACTION METHODS ---
    def action_accept_offer(self):
        """
        Sets the current offer status to Accepted.
        Updates the related property's selling price and buyer.
        Marks all other offers on the same property as Refused.
        """
        for record in self:
            # Ensure only records with properties not canceled can be accepted
            if record.x_property_id.state == 'canceled':
                raise UserError("Canceled properties cannot accept offers.")
            
            # Check if property is already sold
            if record.x_property_id.state == 'sold':
                raise UserError("Cannot accept an offer for a property that is already sold.")
            
            # 1. Refuse all other offers on the same property first
            other_offers = record.x_property_id.x_offer_ids.filtered(
                lambda o: o.id != record.id
            )
            other_offers.write({'x_status': 'refused'})
            
            # 2. Accept the current offer
            record.write({'x_status': 'accepted'})
            
            # 3. Update the property details
            record.x_property_id.write({
                'selling_price': record.x_price,
                'x_partner_id': record.x_partner_id.id,
                'state': 'offer_accepted',
            })
        
        return True
    
    def action_refuse_offer(self):
        """Sets the current offer status to Refused."""
        for record in self:
            if record.x_status != 'refused':
                record.write({'x_status': 'refused'})
                
                # Check if this property has any remaining accepted offers
                remaining_accepted = record.x_property_id.x_offer_ids.filtered(
                    lambda r: r.x_status == 'accepted'
                )
                
                if not remaining_accepted:
                    # If no accepted offers remain, reset property selling details
                    new_state = 'offer_received' if record.x_property_id.x_offer_ids else 'new'
                    
                    record.x_property_id.write({
                        'selling_price': 0.0,
                        'x_partner_id': False,
                        'state': new_state,
                    })
        
        return True
