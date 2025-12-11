from odoo import models, fields

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