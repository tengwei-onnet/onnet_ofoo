from odoo import api, fields, models, _
from odoo.exceptions import UserError


class OSPIndustry(models.Model):
    _name = 'osp.industry'
    _description = 'OSP Industry'
    _order = 'sequence'

    name = fields.Char(string="Name", required=True, index=True)
    sequence = fields.Integer(help="Used to order the OnlineNIC APIs")

    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'Name of the industry must be unique.')
    ]

    def unlink(self):
        for industry in self:
            if industry == \
                    self.env.ref('osp_customization.osp_industry_others'):
                raise UserError(
                    _("You can not delete industry option - Others"))
        return super(OSPIndustry, self).unlink()
