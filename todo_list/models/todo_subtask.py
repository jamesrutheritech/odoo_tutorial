from odoo import models, fields

class TodoSubTask(models.Model):
    _name = "todo.subtask"
    _description = "Subtask of a To-Do Task"

    name = fields.Char("Subtask Title", required=True)
    is_done = fields.Boolean("Done?")
    task_id = fields.Many2one("todo.task", string="Parent Task", required=True)
