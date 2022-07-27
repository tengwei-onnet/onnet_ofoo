odoo.define('upload_video_snippet.s_video', function (require) {
    'use strict';

    var core = require('web.core');
    var weWidgets = require('wysiwyg.widgets');
    var options = require('web_editor.snippets.options');

    var _t = core._t;
    var qweb = core.qweb;

    options.registry.hlcloudVideo = options.Class.extend({
        events: _.extend({}, options.Class.prototype.events, {
            'click we-button.add_video': 'addVideo',
        }),
        /**
         * @override
         */
        start: function () {
            var self = this;
            this.$target.on('dblclick', 'video', function (e) {
                self.addVideo(true);
            });
            return this._super.apply(this, arguments);
        },

        addVideo: function (previewMode) {
            var self = this;
            var media = this.$target.find('video');
            var videoSrc = media.data('oe-expression');
            if (videoSrc.startsWith('/')) {
                media.data('oe-expression', location.origin + videoSrc);
            }
            var dialog = new weWidgets.MediaDialog(this, {noImages: true, noDocuments: true, noIcons: true}, media[0]);
            return new Promise(resolve => {
                dialog.on('save', this, function (data) {
                    var src = $(data).data('oe-expression');
                    var $video = '<video style="width:100%;" autoplay="autoplay" controls="controls" data-oe-expression="' + src + '">\n' +
                        '                    <source src="'+ src +'" type="video/mp4"/>\n' +
                        '                    Your browser does not support the video tag.\n' +
                        '                </video>';
                    self.$target.find('.container').html($video);
                });
                dialog.on('closed', this, () => resolve());
                dialog.open();
            });
        }
    });
});
