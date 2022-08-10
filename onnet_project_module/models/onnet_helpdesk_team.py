# -*- coding: utf-8 -*-
import re

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class OnnetHelpdeskTeam(models.Model):
    _inherit = "helpdesk.team"

    sequence_id = fields.Char(string='Sequence Code')

