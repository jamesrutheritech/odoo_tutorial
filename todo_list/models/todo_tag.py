from odoo import models, fields

class TodoTag(models.Model):
    _name = "todo.tag"
    _description = "To-Do Tag"

    name = fields.Char("Tag Name", required=True)
