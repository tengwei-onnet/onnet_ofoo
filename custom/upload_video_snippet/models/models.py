# -*- coding: utf-8 -*

import logging
_logger = logging.getLogger(__name__)

from odoo import api, fields, models

class VideoVideo(models.Model):

    _name = "video.video"

    name = fields.Char(string="Name")
    data = fields.Binary(string="Data")
    uploader_id = fields.Many2one('res.users', string="Uploader")
    view_count = fields.Integer(string="View Count")
    video_url = fields.Char(compute="compute_video_url", string="URL")

    def compute_video_url(self):
        instance_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        for record in self:
            record.video_url = instance_url + "/videos/stream/" + str(record.id) + ".mp4"
