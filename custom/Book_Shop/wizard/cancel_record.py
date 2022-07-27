import datetime

from odoo import api, fields, models, _


class CancelRecord(models.TransientModel):
    _name = "cancel.record.wizard"
    _description = "Cancel Record"

    @api.model
    def default_get(self, fields):
        res = super(CancelRecord, self).default_get(fields)
        res['date_cancel'] = datetime.date.today()
        if self.env.context.get('active_id'):
            res['record_id'] = self.env.context.get('active_id')
        return res

    record_id = fields.Many2one('onnet.borrow', string="Record",
                                domain=[('borrow_status', 'in', ('returned', 'borrowing'))])
    # filter condition one field with multiple value
    reason = fields.Text(string='Reason')
    date_cancel = fields.Date(string='Date Cancelled')

    def action_cancel(self):
        if self.env.context.get('active_id'):
            form_id = self.env.context.get('active_id')
            self.env['onnet.borrow'].browse(form_id).date_cancel = self.date_cancel
            self.env['onnet.borrow'].browse(form_id).reason = self.reason
            self.env['onnet.borrow'].browse(form_id).borrow_status = 'cancel'
        self.record_id.borrow_status = 'cancel'
        self.record_id.reason = self.reason
        self.record_id.date_cancel = self.date_cancel
        return{
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
