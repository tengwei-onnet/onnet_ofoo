# -*- coding: utf-8 -*-

import base64
import werkzeug
import logging
import json
_logger = logging.getLogger(__name__)

import odoo.http as http
from odoo.addons.http_routing.models.ir_http import slug
from odoo.http import request

class WebsiteVideosController(http.Controller):

    @http.route('/videos/upload/process', type="http", auth="user")
    def videos_upload_process(self, **kwargs):
        create_dict = {}
        create_dict['name'] = kwargs['name']
        create_dict['uploader_id'] = request.env.user.id
        for c_file in request.httprequest.files.getlist('file'):
            create_dict['data'] = base64.b64encode( c_file.read() )
        video = request.env['video.video'].create(create_dict)
        return json.dumps({
            'url': request.httprequest.host_url + 'videos/stream/' + str(video.id) + '.mp4',
            'msg': 'upload success'
        })

    @http.route('/videos/stream/<video>.mp4', type="http", auth="public")
    def videos_stream(self, video):
        """Video Stream"""
        headers = [('Content-Type', 'video/mp4')]
        mainvideo = base64.b64decode(
            request.env['video.video'].browse(int(video)).data)
        status = 200
        if request.httprequest.range:
            contentrange = request.httprequest.range.make_content_range(
                len(mainvideo))
            if contentrange.stop < len(mainvideo):
                status = 206
                headers.append(('Content-Range', 'bytes %s-%s/%s' % (
                    str(contentrange.start), str(contentrange.stop),
                    str(len(mainvideo)))))
            elif contentrange.stop > len(mainvideo):
                status = 416
                mainvideo = ""
            if status != 416:
                mainvideo = mainvideo[contentrange.start:contentrange.stop]
                headers.append(('Content-Length', len(mainvideo)))

        return werkzeug.wrappers.Response(mainvideo, status=status,
                                          headers=headers,
                                          direct_passthrough=True)
        # video_media = request.env['video.video'].browse(int(video)).data
        # headers = [
        #     ('Content-Type', 'video/mp4'),
        # ]
        #
        # return werkzeug.wrappers.Response(base64.b64decode(video_media), headers=headers, direct_passthrough=True)
