# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ToyotaCar(models.Model):
    _name = "toyota.car"
    _description = "Toyota Car"
    name = fields.Char(string='Name')
    ref = fields.Char(string='Reference')
    type = fields.Char(string='Type')
    revenue = fields.Integer(string='Revenue')
    color = fields.Selection([('red', 'Red'), ('blue', 'Blue'), ('green', 'Green')], string='Color')
