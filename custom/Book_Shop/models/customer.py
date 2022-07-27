# -*- coding: utf-8 -*-
import datetime
import math
import re
from datetime import date

from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class OnnetCustomer(models.Model):
    _name = "onnet.customer"
    _description = "Customer"
    _rec_name = 'name'

    name = fields.Char(string='Name', store=True)
    ref = fields.Char(string='Customer Reference', readonly=True, required=True, default=lambda self: _('New'))
    dob = fields.Date(string='Date Of Birth', store=True)
    age = fields.Float(string='Age', compute='_compute_age', inverse='inverse_compute_age', readonly=True, store=True,
                       digits=(3, 0))
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender')
    borrow_id = fields.One2many(comodel_name='onnet.borrow', inverse_name='customer_id', readonly=True)
    phone_no = fields.Char(string="Phone Number", compute='validate_phone_no', store=True)
    is_birthday = fields.Boolean(string='Birthday', compute='validate_birthday', default=False)
    email = fields.Char(string='Email')
    count_borrow = fields.Integer(string='Record Count', compute='count_borrow_record')

    def action_view_record(self):
        return {
            'name': 'Borrow Record',
            'res_model': 'onnet.borrow',
            'view_mode': 'list,form',
            'context': {'default_customer_id': self.id},
            'domain': [('customer_id', '=', self.id)],
            'target': 'current',
            'type': 'ir.actions.act_window',
        }

    @api.depends('borrow_id')
    def count_borrow_record(self):
        for rec in self:
            rec.count_borrow = len(self.borrow_id)

    @api.depends('dob')
    def validate_birthday(self):
        for rec in self:
            is_birthday = False
            if rec.dob:
                today = date.today()
                if today.day == rec.dob.day and today.month == rec.dob.month:
                    is_birthday = True
            rec.is_birthday = is_birthday

    @api.depends('age')
    def inverse_compute_age(self):
        today = date.today()
        for rec in self:
            rec.dob = today - relativedelta(years=rec.age)

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        if default is None:
            default = {}
        if not default.get('ref'):
            default['ref'] = self.ref + " (copy)"
        return super(OnnetCustomer, self).copy(default)

    _sql_constraints = [
        ('unique_ref', 'unique(ref)', 'Reference Number must be unique')
    ]

    @api.constrains('dob')
    def validate_dob(self):
        for rec in self:
            if rec.dob and rec.dob > fields.Date.today():
                raise ValidationError("Invalid Date of Birth, Please Enter Again")

    @api.constrains('phone_no')
    def validate_phone_no(self):
        if self.phone_no:
            match = re.match("(\\d{3}-\\d{7,8})", self.phone_no)
            if not match:
                raise ValidationError('Invalid Phone Number, Please follow this format "XXX-XXXXXXX"\neg: 016-9289983')

    @api.model
    def create(self, vals):
        if vals.get('ref', _('New')) == _('New'):
            vals['ref'] = self.env['ir.sequence'].next_by_code(
                'onnet.customer') or _('New')
        res = super(OnnetCustomer, self).create(vals)
        return res

    def write(self, vals):
        if not self.ref and not vals.get('ref'):
            vals['ref'] = self.env['ir.sequence'].next_by_code(
                'onnet.customer') or _('New')
        return super(OnnetCustomer, self).write(vals)

    @api.depends('dob')
    def _compute_age(self):
        for doc in self:
            if doc.dob:
                years = relativedelta(date.today(), doc.dob).years
                months = relativedelta(date.today(), self.dob).months
                day = relativedelta(date.today(), self.dob).days
                doc.age = int(years)
            else:
                doc.age = 0

    def add_record(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'onnet.borrow',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('Book_Shop.view_onnet_borrow_form').id,
            'target': 'new',
            'context': {'customer_id': self.id}
        }

    def name_get(self):
        return [(record.id, "(%s) %s" % (record.ref, record.name)) for record in self]

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        args = list(args or [])
        if name:
            args += ['|', ('name', operator, name),
                     ('ref', operator, name)]
        return self._search(args, limit=limit, access_rights_uid=name_get_uid)
