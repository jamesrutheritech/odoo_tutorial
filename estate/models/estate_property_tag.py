# estate/models/estate_property_tag.py

from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = 'x_estate.property.tag'  # CORRECTED: Added 'x_' prefix
    _description = 'Real Estate Property Tag'
    _order = "name" 

    name = fields.Char(required=True)
    color = fields.Integer()