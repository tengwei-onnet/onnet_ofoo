from odoo import api, fields, models, _


class SaleOrder(models.Model):
    _name = "sale.order"
    _description = "Sale Order"
    _inherit = 'sale.order'
    record_id = fields.Many2many('onnet.borrow', string='Record ID')
