from datetime import datetime, date
from time import localtime
import pytz
import re

from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class OnnetStaff(models.Model):
    _name = "onnet.staff"
    _description = "Bookshop Staff"
    _rec_name = 'name'

    name = fields.Char(string='Staff Name')
    ref = fields.Char(string='Staff Reference', required=True, readonly=True, default=lambda self: _('New'))
    dob = fields.Date(string='Date Of Birth')
    age = fields.Float(string='Age', compute='_compute_age', store=True, digits=(3, 0))
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender')
    position = fields.Char(string='Position')
    salary = fields.Monetary(string='Salary', currency_field="currency_id")
    currency_id = fields.Many2one("res.currency", string="Valuta")
    attendance_id = fields.One2many(comodel_name='onnet.attendance', inverse_name='staff_id', readonly=True)
    active = fields.Boolean(string='Active', default=True, readonly=True)
    phone_no = fields.Char(string="Phone Number", compute='validate_phone_no', store=True)

    @api.constrains('phone_no')
    def validate_phone_no(self):
        for staff in self:
            if staff.phone_no:
                match = re.match("(\\d{3}-\\d{7,8})", staff.phone_no)
                if not match:
                    raise ValidationError('Invalid Phone Number, Please follow this format "XXX-XXXXXXX"\neg: 016-9289983')

    @api.model
    def create(self, vals):
        if vals.get('ref', _('New')) == _('New'):
            vals['ref'] = self.env['ir.sequence'].next_by_code(
                'onnet.staff') or _('New')
        res = super(OnnetStaff, self).create(vals)
        return res

    def write(self, vals):
        if not self.ref and not vals.get('ref'):
            vals['ref'] = self.env['ir.sequence'].next_by_code(
                'onnet.staff') or _('New')
        return super(OnnetStaff, self).write(vals)

    @api.depends('dob')
    def _compute_age(self):
        for staff in self:
            if staff.dob:
                years = relativedelta(date.today(), staff.dob).years
                months = relativedelta(date.today(), self.dob).months
                day = relativedelta(date.today(), self.dob).days
                staff.age = int(years)
            else:
                staff.age = 0

    def name_get(self):
        res = []
        for record in self:
            res.append((record.id, "(%s) %s" % (record.ref, record.name)))
        return res

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        args = list(args or [])
        if name:
            args += ['|', ('name', operator, name),
                     ('ref', operator, name)]
        return self._search(args, limit=limit, access_rights_uid=name_get_uid)


class StaffAttendance(models.Model):
    _name = "onnet.attendance"
    _description = "Staff Attendance"
    _rec_name = 'staff_id'

    staff_id = fields.Many2one(comodel_name='onnet.staff', string='Staff ID', store=True, tracking=True)
    check_in = fields.Char(string='Check In', store=True, readonly=True)
    check_out = fields.Char(string='Check Out', store=True, readonly=True)
    date_check_in = fields.Date(store=True)

    def action_check_in(self):
        for check in self:
            tz_Malaysia = pytz.timezone('Asia/Kuala_Lumpur')
            now = datetime.now(tz_Malaysia)
            # dd/mm/YY H:M:S
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            check.check_in = dt_string
            check.date_check_in = date.today()

    def action_check_out(self):
        for check in self:
            tz_Malaysia = pytz.timezone('Asia/Kuala_Lumpur')
            now = datetime.now(tz_Malaysia)
            # dd/mm/YY H:M:S
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            check.check_out = dt_string
