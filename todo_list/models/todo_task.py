from odoo import api, fields, models
from odoo.exceptions import ValidationError
from datetime import timedelta


class TodoTask(models.Model):
    _name = "todo.task"
    _description = "To-Do Task"

    _sql_constraints = [
        ('check_estimated_hours_positive',
         'CHECK(estimated_hours >= 0)',
         'Estimated hours must be positive!'),
        ('check_progress_range',
         'CHECK(progress >= 0 AND progress <= 100)',
         'Progress must be between 0 and 100!'),
        ('unique_task_name',
         'UNIQUE(name)',
         'Task title must be unique!')
    ]

    name = fields.Char("Task Title", required=True)
    description = fields.Text("Description")
    is_done = fields.Boolean("Done?")
    priority = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ], string="Priority", default='medium')
    start_date = fields.Date("Start Date") 
    due_date = fields.Date("Due Date")
    estimated_hours = fields.Float("Estimated Time (H:M)") 
    progress = fields.Integer("Progress", default=0)
    
    category_id = fields.Many2one("todo.category", string="Category")
    tag_ids = fields.Many2many(
        "todo.tag", "todo_task_tag_rel",
        "task_id", "tag_id",
        string="Tags"
    )
    
    tag_names = fields.Char(
        string="Tags Summary",
        compute="_compute_tag_names",
        store=True
    )
    state = fields.Selection([
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('done', 'Done')
    ], string="Status", default='new')
    notes = fields.Text("Notes")

    @api.depends('tag_ids')
    def _compute_tag_names(self):
        for task in self:
            task.tag_names = ", ".join(task.tag_ids.mapped('name'))
            
    @api.onchange('progress')
    def _onchange_progress_update_state(self):
        if self.progress == 100:
            self.state = 'done'
            self.is_done = True
        elif self.progress == 0:
            self.state = 'new'
            self.is_done = False
        elif 0 < self.progress < 100:
            self.state = 'in_progress'
            self.is_done = False

    @api.onchange('start_date')
    def _onchange_start_date(self):
        if self.start_date and not self.due_date:
            self.due_date = self.start_date + timedelta(days=7) 

    @api.constrains('start_date', 'due_date')
    def _check_dates(self):
        for task in self:
            if task.start_date and task.due_date:
                if task.due_date < task.start_date:
                    raise ValidationError("Due date cannot be earlier than start date.")

    @api.constrains('estimated_hours')
    def _check_minimum_estimated_hours(self):
        MINIMUM_HOURS = 0.25  
        for task in self:
            if task.estimated_hours > 0 and task.estimated_hours < MINIMUM_HOURS:
                raise ValidationError("Estimated Time must be at least 15 minutes (0:15).")

    def write(self, vals):
        for task in self:
            if vals.get('state') == 'done':
                vals['progress'] = 100
        return super(TodoTask, self).write(vals)

    def unlink(self): 
        for task in self:
            if task.is_done:
                raise ValidationError("Cannot delete a task that is done!")
        return super(TodoTask, self).unlink()

    def action_mark_done(self):
        for task in self:
            task.write({
                'progress': 100,
                'state': 'done',
                'is_done': True,
            })


class TodoCategory(models.Model):
    _name = "todo.category"
    _description = "To-Do Category"
    name = fields.Char("Category Name", required=True)

class TodoTag(models.Model):
    _name = "todo.tag"
    _description = "To-Do Tag"
    name = fields.Char("Tag Name", required=True)