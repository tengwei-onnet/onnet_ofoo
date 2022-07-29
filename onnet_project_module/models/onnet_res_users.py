# -*- coding: utf-8 -*-
import re

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class OnnetUser(models.Model):
    _inherit = "res.users"

    phone_no = fields.Char(string="Phone Number", store=True)

    @api.constrains('phone_no')
    def validate_phone_no(self):
        if self.phone_no:
            match = re.match("(\\d{3}-\\d{7,8})", self.phone_no)
            if not match:
                raise ValidationError('Invalid Phone Number, Please follow this format "XXX-XXXXXXX"\neg: 016-9289983')
