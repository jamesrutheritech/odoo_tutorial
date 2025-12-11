from odoo import models, fields, api
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = 'x_estate.property.offer'
    _description = 'Real Estate Property Offer'
    
    # Required Fields
    x_price = fields.Float(required=True)
    
    x_status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        copy=False
    )
    
    # Relationships 
    x_partner_id = fields.Many2one('res.partner', required=True, string="Partner")
    
    # Many2one link back to the parent property (estate.property)
    x_property_id = fields.Many2one('estate.property', required=True, string="Property") 
    
    # --- Action Methods ---

    def action_accept_offer(self):
        """
        Sets the current offer status to Accepted.
        Updates the related property's selling price and buyer.
        Marks all other offers on the same property as Refused.
        """
        # Ensure only records with status 'new' can be accepted
        if self.x_property_id.state == 'canceled':
            raise UserError("Canceled properties cannot accept offers.")
        
        # 1. Refuse all other offers on the same property first
        # Filter all offers on the same property that are NOT the current record
        other_offers = self.x_property_id.x_offer_ids.filtered(
            lambda o: o != self
        )
        other_offers.write({'x_status': 'refused'})

        # 2. Update the property details
        self.x_property_id.write({
            'selling_price': self.x_price,
            'x_partner_id': self.x_partner_id.id,
            'state': 'offer_accepted',
        })
        
        # 3. Accept the current offer
        self.write({'x_status': 'accepted'})
        
        return True
    
    def action_refuse_offer(self):
        """Sets the current offer status to Refused."""
        self.write({'x_status': 'refused'})
        
        # Optional: Reset property state if the previously accepted offer is refused
        # You could add logic here to check the property state.
        
        return True