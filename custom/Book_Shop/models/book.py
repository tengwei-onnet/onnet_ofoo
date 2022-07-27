# -*- coding: utf-8 -*-
import datetime
import math
from datetime import date

from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class BookCategory(models.Model):
    _name = "book.category"
    _description = "Book Category"

    name = fields.Char(string='Category')
    color = fields.Integer()

    _sql_constraints = [
        ('unique_category_name', 'unique(name)', 'Name must be unique')
    ]


class OnnetBook(models.Model):
    _name = "onnet.book"
    _description = "Book"
    _rec_name = 'title'

    title = fields.Char(string='Title')
    ref = fields.Char(string='Book Reference', required=True, readonly=True, default=lambda self: _('New'))
    author = fields.Char(string='Author')
    description = fields.Text(string='Description')
    category_id = fields.Many2many('book.category', string='Category')
    price = fields.Monetary(string='Price', currency_field="currency_id")
    currency_id = fields.Many2one("res.currency", string="Valuta")
    page = fields.Integer(string='Page')
    borrow_id = fields.Many2many(comodel_name='onnet.borrow',
                                 relation='book_borrowed',
                                 column1='book_id',
                                 column2='borrow_id',
                                 readonly=True)
    image = fields.Binary(string="Image")
    rating = fields.Selection([
        ('0', 'Thrash'),
        ('1', 'Bad'),
        ('2', 'Normal'),
        ('3', 'Good'),
        ('4', 'Excellent'),
        ('5', 'Perfect')], string="Rating", help="Rate this Book ^^")
    reference_record = fields.Reference(selection=[('onnet.customer', 'Customer'),
                                                   ('onnet.staff', 'Staff')],
                                        string="Customer ID")

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        if default is None:
            default = {}
        if not default.get('ref'):
            default['ref'] = self.env['ir.sequence'].next_by_code('onnet.book')
        return super(OnnetBook, self).copy(default)

    _sql_constraints = [
        ('unique_ref', 'unique(ref)', 'Reference Number must be unique')
    ]

    @api.model
    def create(self, vals):
        if vals.get('ref', _('New')) == _('New'):
            vals['ref'] = self.env['ir.sequence'].next_by_code(
                'onnet.book') or _('New')
        res = super(OnnetBook, self).create(vals)
        return res


class Stage(models.Model):
    _name = "borrow.category"
    _description = "borrow Category"

    name = fields.Char(string='Stage')
    color = fields.Integer()


class OnnetBorrow(models.Model):
    _name = "onnet.borrow"
    _inherit = ["mail.thread"]
    _description = "Borrow Date"
    _rec_name = 'ref'

    @api.model
    def default_get(self, fields):
        res = super(OnnetBorrow, self).default_get(fields)
        if self.env.context.get('active_id'):
            res['customer_id'] = self.env.context.get('active_id')
        return res

    ref = fields.Char(string='Book Reference', required=True, readonly=True, default=lambda self: _('New'))
    customer_id = fields.Many2one(comodel_name='onnet.customer', string='Customer ID', store=True, tracking=True)
    customer_name = fields.Char(related='customer_id.name', string='Customer Name')
    book_id = fields.Many2many(comodel_name='onnet.book',
                               relation='book_borrowed',
                               column1='borrow_id',
                               column2='book_id',
                               tracking=True)
    borrowDate = fields.Date(string='Borrow Date', tracking=True, default=fields.Date.context_today)
    dueDate = fields.Date(string='Due Date', compute='calculate_due_date', tracking=True)
    borrow_status = fields.Selection([('draft', 'Draft'), ('borrowing', 'Borrowing'), ('returned', 'Returned'),
                                      ('cancel', 'Cancelled')], default='draft', copy=False, tracking=True)
    is_penalty = fields.Boolean(string='Penalty', compute='check_penalty', default=False, store=True)
    penalty_fee = fields.Float(string='Penalty Fee', compute='calculate_penalty_fee', default=0, digits=(8, 2))
    returnDate = fields.Date(string='Return Date', tracking=True, store=True, compute='_compute_return_date')
    phone_no = fields.Char(string="Phone Number", related='customer_id.phone_no')
    date_cancel = fields.Date(string='Cancelled Date', tracking=True)
    reason = fields.Text(string='Reason', tracking=True)
    fee = fields.Float(string='Fee (RM5 per book)', digits=(8, 2),
                       compute='calculate_fee', tracking=True)
    customer_dob = fields.Boolean(string='Birthday', compute='validate_dob', default=False)
    currency_id = fields.Many2one('res.currency', related='book_id.currency_id')
    total_price = fields.Monetary(string='Total Price', compute='calculate_total_price', default=0, tracking=True, store=True)
    color = fields.Integer()
    active = fields.Boolean(string='Active', default=True, readonly=True)

    @api.depends('borrow_status')
    def _compute_return_date(self):
        for lead in self:
            if lead.borrow_status == 'returned':
                lead.returnDate = fields.Datetime.now()

    @api.depends('fee', 'is_penalty')
    def calculate_total_price(self):
        total_price = 0
        for cus in self:
            if cus.fee and cus.is_penalty:
                total_price = cus.fee + cus.penalty_fee
            elif not cus.is_penalty:
                total_price += cus.fee
            cus.total_price = total_price

    def validate_dob(self):
        for cus in self:
            cus.customer_dob = False
            if cus.customer_id.dob and cus.customer_id.dob.day == cus.borrowDate.day and cus.customer_id.dob.month == cus.borrowDate.month:
                cus.customer_dob = True

    @api.depends('book_id')
    def count_books(self):
        return len(self.book_id)

    def calculate_fee(self):
        for price in self:
            if price.customer_dob:
                price.fee = (price.count_books() - 1) * 5
            else:
                price.fee = price.count_books() * 5

    def action_send_whatsapp(self):
        if not self.phone_no:
            raise ValidationError("Missing phone number in this record")

        new_str = self.customer_id.phone_no
        valid_phone_no = new_str.replace("-", "")

        msg = "Hi " + self.customer_id.name + \
              ", Here is _Onnet BookShop_ ^^. %0aWe checked that your borrowing record *" + \
              self.ref + "* is expired. " \
                         "Please return the book as soon as possible before receiving a penalty of RM5 per day. " \
                         "%0aRecord ID:%09" + self.ref + "%0aCustomer:%09" + self.customer_id.name + \
              "%0aBorrow Date:%09" + str(self.borrowDate) + "%0aDue Date:%09" + str(self.dueDate)

        whatsapp_url = 'https://api.whatsapp.com/send?phone=+6' + valid_phone_no + '&text=' + msg

        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': whatsapp_url
        }

    # def unlink(self):
    #     for rec in self:
    #         rec_set = self.env['onnet.borrow'].search([('id', 'in', rec)])
    #         if rec_set.borrow_status == 'borrowing':
    #             raise ValidationError("Cannot Delete Record in Borrowing Status!!!")
    #         elif rec_set.borrow_status == 'returned':
    #             raise ValidationError("Cannot Delete Record in Returned Status!!!")
    #         else:
    #             rec_set.unlink()

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        if default is None:
            default = {}
        if not default.get('ref'):
            default['ref'] = self.ref + " (copy)"
            default['borrow_status'] = 'draft'
        return super(OnnetBorrow, self).copy(default)

    _sql_constraints = [
        ('unique_ref', 'unique(ref)', 'Reference Number must be unique')
    ]

    def return_book(self):
        for rec in self:
            rec.borrow_status = 'returned'
            rec.returnDate = date.today()
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Customer Returned the Books',
                'type': 'rainbow_man',
            }
        }

    def borrowing_book(self):
        for rec in self:
            rec.borrow_status = 'borrowing'
            rec.date_cancel = None
            rec.returnDate = None
            rec.is_penalty = False

    def cancel_record(self):
        for rec in self:
            action = rec.env.ref('Book_Shop.action_cancel_record').read()[0]  # self.env.ref is to read xml id
            return action

    def set_draft(self):
        for rec in self:
            rec.borrow_status = 'draft'
            rec.date_cancel = None

    @api.model
    def create(self, vals):
        if vals.get('ref', _('New')) == _('New'):
            vals['ref'] = self.env['ir.sequence'].next_by_code(
                'onnet.borrow') or _('New')
        res = super(OnnetBorrow, self).create(vals)
        return res

    @api.depends('borrowDate')
    def calculate_due_date(self):
        for doc in self:
            if doc.borrowDate:
                doc.dueDate = doc.borrowDate + datetime.timedelta(days=14)  # 2 weeks due date
            else:
                doc.borrowDate = date.today()
                doc.dueDate = doc.borrowDate + datetime.timedelta(days=14)

    @api.depends('returnDate')
    def check_penalty(self):
        for penalty in self:
            if penalty.returnDate and penalty.dueDate:
                penalty.is_penalty = (penalty.returnDate > penalty.dueDate)

    def calculate_penalty_fee(self):
        for penalty in self:
            if penalty.is_penalty:
                today = date.today()
                due_date = penalty.dueDate
                count_day = today - due_date
                penalty.penalty_fee = count_day.days * 5
            else:
                penalty.penalty_fee = 0.00

    @api.constrains('returnDate')
    def validate_return_date(self):
        if self.returnDate and self.returnDate < self.borrowDate:
            raise ValidationError("Return Date cannot be set before Borrow Date!!!")
