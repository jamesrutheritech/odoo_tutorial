from odoo import models, fields

class TodoCategory(models.Model):
    _name = "todo.category"
    _description = "Task Category"

    name = fields.Char("Category Name", required=True)
    task_ids = fields.One2many("todo.task", "category_id", string="Tasks")
