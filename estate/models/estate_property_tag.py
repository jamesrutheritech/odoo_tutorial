from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Real Estate Property Tag'
    _order = "name" # Added ordering for better usability

    name = fields.Char(required=True)
    color = fields.Integer() # Added this field to support the color_picker widget in the view