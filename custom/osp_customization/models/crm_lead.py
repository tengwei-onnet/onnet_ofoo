from odoo import api, fields, models, SUPERUSER_ID
from datetime import date


class Lead(models.Model):
    _inherit = 'crm.lead'

    industry = fields.Char(string='Old Industry (Deprecated)')
    industry_id = fields.Many2one("osp.industry", string="Industry")
    industry_ref = fields.Char(string='Industry Reference')
    medium_ref = fields.Char(string='Medium Reference',
                             default="Contact us")
    preferred_module = fields.Char(string='Preferred Module')
    customer_requirement = fields.Char(string='Customer Requirement')
    solution_type = fields.Char(string='Solution Type')
    timeline = fields.Char(string='Timeline')
    no_of_employee = fields.Char(string='Number of Employee in Range')
    annual_revenue = fields.Char(string='Annual Revenue in Range')
    # partner_name = fields.Char
    # function = fields.Char(required=True)
    # phone = fields.Char
    first_time_user = fields.Char(string='First Time User')
    first_time_odoo = fields.Boolean(string='First Time User', default=False)
    category = fields.Char(string='Category')
    business_modal = fields.Selection([('b2b', 'B2B'), ('b2c', 'B2C')], string='Business Model',
        help='Customer Business Modal (B2C/B2C)')
    date_lost = fields.Date(string="Lost Date", copy=False, store=True)

    # def action_set_won(self):
    #     self.date_closed = date.today()
    #     super(Lead, self).action_set_won()
    #
    # def action_set_lost(self, **additional_values):
    #     for lost in self:
    #         if lost.lost_reason:
    #             lost.date_lost = date.today()
    #         else:
    #             lost.date_lost = False
    #     super(Lead, self).action_set_lost(**additional_values)
    #
    # def toggle_active(self):
    #     self.date_lost = None
    #     super(Lead, self).toggle_active()

    @api.model
    def create(self, vals):
        # if 'name' in vals:
        #     vals['partner_name'] = vals['name']
        if 'first_time_user' in vals and vals['first_time_user'] == 'True':
            vals['first_time_odoo'] = True
        return super(Lead, self).create(vals)
