# estate/models/estate_property.py

from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'
    _order = "id desc"

    # ... [Field Definitions remain the same] ...
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False,
        default=lambda self: fields.Date.add(fields.Date.today(), months=3)
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer() # Keep as Integer
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ]
    )
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled')
        ],
        default='new',
        required=True,
        copy=False
    )
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    salesperson_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    
    total_area = fields.Float(compute="_compute_total_area", store=True)
    best_price = fields.Float(compute="_compute_best_price", store=True)

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for prop in self:
            prop.total_area = prop.living_area + prop.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for prop in self:
            if prop.offer_ids:
                prop.best_price = max(prop.offer_ids.mapped('price'))
            else:
                prop.best_price = 0.0

    @api.onchange("garden")
    def _onchange_garden(self):
        # Implementation for Exercise 2: Reset on uncheck
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False # Resetting to False
            
    # --- UPDATED action_sold METHOD (Exercise 1 Constraint) ---

    def action_sold(self):
        """
        Marks property as sold.
        Constraint 1: Must have accepted offers.
        """
        self.check_access(['write'])
        
        for record in self:
            if record.state == 'canceled':
                raise UserError("Canceled properties cannot be sold.")
            
            # --- NEW CONSTRAINT FOR UNIT TEST EXERCISE ---
            accepted_offers = record.offer_ids.filtered(lambda o: o.status == 'accepted')
            if not accepted_offers:
                 raise UserError("You must have at least one accepted offer to sell a property.")
            # ---------------------------------------------

            if record.state == 'offer_accepted' and (not record.buyer_id or not record.selling_price):
                # Note: This check should logically come after checking for accepted offers,
                # or should be handled by the offer acceptance process.
                raise UserError(
                    "You must have a Buyer and Selling Price set before marking the property as sold."
                )

            # --- SECURITY BYPASS (SUDO) FOR INVOICE CREATION ---
            if 'account.move' in self.env:
                self.env['account.move'].sudo().create({
                    'partner_id': record.buyer_id.id,
                    'move_type': 'out_invoice',
                    'invoice_line_ids': [
                        (0, 0, {
                            'name': f"Selling Property: {record.name} (Commission)",
                            'quantity': 1,
                            'price_unit': record.selling_price * 0.06,
                        }),
                        (0, 0, {
                            'name': 'Administrative Fees',
                            'quantity': 1,
                            'price_unit': 100.00,
                        }),
                    ],
                })
            
            record.state = 'sold'
        return True

    def action_cancel(self):
        """Cancel property"""
        for record in self:
            if record.state == 'sold':
                raise UserError("Sold properties cannot be canceled.")
            record.state = 'canceled'
        return True

    @api.constrains("expected_price", "selling_price")
    def _check_price_difference(self):
        for record in self:
            if float_compare(record.selling_price, 0.0, precision_digits=2) != 0 and \
               float_compare(record.selling_price, record.expected_price * 0.9, precision_digits=2) < 0:
                raise UserError("The selling price cannot be lower than 90% of the expected price.")

    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_or_canceled(self):
        for record in self:
            if record.state not in ('new', 'canceled'):
                raise UserError("Only new or canceled properties can be deleted.")