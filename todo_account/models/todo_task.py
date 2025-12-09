from odoo import api, fields, models
from odoo.exceptions import UserError

class TodoTask(models.Model):
    _inherit = "todo.task"

    invoice_id = fields.Many2one('account.move', string='Generated Invoice', readonly=True)

    def action_mark_done(self):
        """
        Overrides the standard action to mark a task done and create an invoice.
        """
        res = super(TodoTask, self).action_mark_done()

        for task in self.filtered(lambda t: t.is_done and not t.invoice_id):
            
            partner = self.env['res.partner'].search([('is_company', '=', True)], limit=1)
            
            if not partner:
                raise UserError("Cannot create invoice: No customer found in the system.")

            invoice_line_vals = [(0, 0, {
                'name': f"Service for Task: {task.name}",
                'quantity': 1,
                'price_unit': task.estimated_hours * 50,
            })]

            invoice = self.env['account.move'].create({
                'partner_id': partner.id,
                'move_type': 'out_invoice', 
                'invoice_date': fields.Date.today(),
                'invoice_line_ids': invoice_line_vals,
            })
            
            task.invoice_id = invoice.id

        return res