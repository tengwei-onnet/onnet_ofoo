odoo.define('upload_video_snippet.wysiwyg.widgets.media', function (require) {
    'use strict';

    var MediaModules = require('wysiwyg.widgets.media');
    var core = require('web.core');
    var _t = core._t;
    var media = require('wysiwyg.widgets.media');


    // media.MediaWidget.include({
    //     start: function () {
    //         var self = this;
    //         return this._super.apply(this, arguments).then(function () {
    //             self.$('.o_video_dialog_options').after('<div class="upload-area">\n' +
    //                 '                    <label class="col-form-label" for="o_video_text">\n' +
    //                 '                        other upload methods\n' +
    //                 '                    </label>\n' +
    //                 '                    <div id="videoDragDrop">\n' +
    //                 '                        <button type="button" class="btn btn-primary upload-trigger">upload video</button>\n' +
    //                 '                    </div>\n' +
    //                 '                </div>');
    //         });
    //     }
    // });

    MediaModules.VideoWidget.include({

        // events: _.extend({}, MediaModules.VideoWidget.prototype.events || {}, {
        //     'click .upload-trigger': '_openVideoUploadModal',
        // }),

        // _openVideoUploadModal: function () {
        //     this.uppy.getPlugin('Dashboard').openModal();
        // },

        // start: function () {
        //     var self = this;
        //     return this._super.apply(this, arguments).then(function () {
        //         //    use uppy to handle upload video
        //         var uppy = Uppy.Core({
        //             debug: true,
        //             meta: {
        //                 csrf_token: core.csrf_token
        //             },
        //             autoProceed: true,
        //             locale: Uppy.locales.en_US,
        //             allowMultipleUploads: false,
        //             restrictions: {
        //                 maxNumberOfFiles: 1,
        //                 allowedFileTypes: ['video/*', '.mp4']
        //             },
        //         });
        //         uppy.use(Uppy.Dashboard, {
        //             // trigger: '.upload-trigger',
        //             closeAfterFinish: true,
        //             inline: false,
        //             proudlyDisplayPoweredByUppy: false,
        //             showProgressDetails: true
        //         });
        //         uppy.use(Uppy.Webcam, {
        //             target: Uppy.Dashboard,
        //             // title: '摄像头(https)'
        //         });
        //         uppy.use(Uppy.ScreenCapture, {
        //             target: Uppy.Dashboard,
        //             // title: '屏幕录制'
        //         });
        //         uppy.use(Uppy.XHRUpload, {
        //             endpoint: location.origin + '/videos/upload/process',
        //             fieldName: 'file'
        //         });
        //         uppy.on('upload-success', (file, response) => {
        //             // HTTP status code
        //             // extracted response data
        //             const videoUrl = response.body.url;
        //             self._updateVideoViaUrl(videoUrl);
        //         });
        //         self.uppy = uppy;
        //     });
        // },
        _updateVideo: function () {
            // Reset the feedback
        this.$content.empty();
        this.$('#o_video_form_group').removeClass('o_has_error o_has_success').find('.form-control, .custom-select').removeClass('is-invalid is-valid');
        this.$('.o_video_dialog_options div').addClass('d-none');

        // Check video code
        var $textarea = this.$('textarea#o_video_text');
        var code = $textarea.val().trim();
        if (!code) {
            return;
        }

        // Detect if we have an embed code rather than an URL
        var embedMatch = code.match(/(src|href)=["']?([^"']+)?/);
        if (embedMatch && embedMatch[2].length > 0 && embedMatch[2].indexOf('instagram')) {
            embedMatch[1] = embedMatch[2]; // Instagram embed code is different
        }
        var url = embedMatch ? embedMatch[1] : code;

        var query = this._createVideoNode(url, {
            'autoplay': this.isForBgVideo || this.$('input#o_video_autoplay').is(':checked'),
            'hide_controls': this.isForBgVideo || this.$('input#o_video_hide_controls').is(':checked'),
            'loop': this.isForBgVideo || this.$('input#o_video_loop').is(':checked'),
            'hide_fullscreen': this.isForBgVideo || this.$('input#o_video_hide_fullscreen').is(':checked'),
            'hide_yt_logo': this.isForBgVideo || this.$('input#o_video_hide_yt_logo').is(':checked'),
            'hide_dm_logo': this.isForBgVideo || this.$('input#o_video_hide_dm_logo').is(':checked'),
            'hide_dm_share': this.isForBgVideo || this.$('input#o_video_hide_dm_share').is(':checked'),
        });

        console.log(query);
        var $optBox = this.$('.o_video_dialog_options');

        // Show / Hide preview elements
        this.$el.find('.o_video_dialog_preview_text, .media_iframe_video_size').add($optBox).toggleClass('d-none', !query.$video);
        // Toggle validation classes
        this.$el.find('#o_video_form_group')
            .toggleClass('o_has_error', !query.$video).find('.form-control, .custom-select').toggleClass('is-invalid', !query.$video)
            .end()
            .toggleClass('o_has_success', !!query.$video).find('.form-control, .custom-select').toggleClass('is-valid', !!query.$video);

        // Individually show / hide options base on the video provider
        $optBox.find('div.o_' + query.type + '_option').removeClass('d-none');

        // Hide the entire options box if no options are available or if the
        // dialog is opened for a background-video
        $optBox.toggleClass('d-none', this.isForBgVideo || $optBox.find('div:not(.d-none)').length === 0);

        if (query.type === 'youtube') {
            // Youtube only: If 'hide controls' is checked, hide 'fullscreen'
            // and 'youtube logo' options too
            this.$('input#o_video_hide_fullscreen, input#o_video_hide_yt_logo').closest('div').toggleClass('d-none', this.$('input#o_video_hide_controls').is(':checked'));
        }
        if (query.type === 'cdn'){
            console.log("=====>>", this);
                this.$el.find('.media_iframe_video_size').addClass('custom_video_size');
            }
        var $content = query.$video;
        if (!$content) {
            switch (query.errorCode) {
                case 0:
                    $content = $('<div/>', {
                        class: 'alert alert-danger o_video_dialog_iframe mb-2 mt-2',
                        text: _t("The provided url is not valid"),
                    });
                    break;
                case 1:
                    $content = $('<div/>', {
                        class: 'alert alert-warning o_video_dialog_iframe mb-2 mt-2',
                        text: _t("The provided url does not reference any supported video"),
                    });
                    break;
            }
        }
        this.$content.replaceWith($content);
        this.$content = $content;



        },
        _updateVideoViaUrl: function (url) {
            var query = this._createVideoNode(url, {
                'autoplay': this.isForBgVideo || this.$('input#o_video_autoplay').is(':checked'),
                'hide_controls': this.isForBgVideo || this.$('input#o_video_hide_controls').is(':checked'),
                'loop': this.isForBgVideo || this.$('input#o_video_loop').is(':checked'),
                'hide_fullscreen': this.isForBgVideo || this.$('input#o_video_hide_fullscreen').is(':checked'),
                'hide_yt_logo': this.isForBgVideo || this.$('input#o_video_hide_yt_logo').is(':checked'),
                'hide_dm_logo': this.isForBgVideo || this.$('input#o_video_hide_dm_logo').is(':checked'),
                'hide_dm_share': this.isForBgVideo || this.$('input#o_video_hide_dm_share').is(':checked'),
            });
            console.log("==>>>", query)

            var $optBox = this.$('.o_video_dialog_options');

            // Show / Hide preview elements
            this.$el.find('.o_video_dialog_preview_text, .media_iframe_video_size').add($optBox).toggleClass('d-none', !query.$video);
            // Toggle validation classes
            this.$el.find('#o_video_form_group')
                .toggleClass('o_has_error', !query.$video).find('.form-control, .custom-select').toggleClass('is-invalid', !query.$video)
                .end()
                .toggleClass('o_has_success', !!query.$video).find('.form-control, .custom-select').toggleClass('is-valid', !!query.$video);

            // Individually show / hide options base on the video provider
            $optBox.find('div.o_' + query.type + '_option').removeClass('d-none');

            // Hide the entire options box if no options are available or if the
            // dialog is opened for a background-video
            $optBox.toggleClass('d-none', this.isForBgVideo || $optBox.find('div:not(.d-none)').length === 0);

            if (query.type === 'youtube') {
                // Youtube only: If 'hide controls' is checked, hide 'fullscreen'
                // and 'youtube logo' options too
                this.$('input#o_video_hide_fullscreen, input#o_video_hide_yt_logo').closest('div').toggleClass('d-none', this.$('input#o_video_hide_controls').is(':checked'));
            }
            if (query.type == 'cdn'){

                this.$('media_iframe_video_size').addClass('custom_video_size');
            }
            console.log($content);
            console.log( query);
            var $content = query.$video;
            if (!$content) {
                switch (query.errorCode) {
                    case 0:
                        $content = $('<div/>', {
                            class: 'alert alert-danger o_video_dialog_iframe mb-2 mt-2',
                            text: _t("The provided url is not valid"),
                        });
                        break;
                    case 1:
                        $content = $('<div/>', {
                            class: 'alert alert-warning o_video_dialog_iframe mb-2 mt-2',
                            text: _t("The provided url does not reference any supported video"),
                        });
                        break;
                }
            }
            this.$content.replaceWith($content);
            this.$content = $content;
            this.$('textarea#o_video_text').val(url);
        },
        // save: function () {
        //     var self = this;

        //     return this._super(...arguments).then(function (data) {
        //         const videoSrc = self.$content.attr('src');
        //         // if (videoSrc.endsWith('mp4')) {
        //         //     $(data).find('.media_iframe_video_size').addClass('custom_video_size');
        //         // } else {
        //         //     $(data).find('.media_iframe_video_size').removeClass('custom_video_size');
        //         // }
        //         return $(data)[0];
        //     });
        // },

        save: function () {
            this._updateVideo();
            
            if (this.isForBgVideo) {
                return Promise.resolve({bgVideoSrc: this.$content.attr('src')});
            }
            console.log("--->>>this-000>>", this.$content[0]);
            const videoSrc = this.$content.attr('data-oe-expression');
            console.log("-----SAVE CALLEED=====>", videoSrc);
            if (videoSrc) {
                if (videoSrc.endsWith('mp4')) {
                    this.$media = $(
                        '<div class="media_iframe_video" data-oe-expression="' + this.$content.attr('data-oe-expression') + '">' +
                            '<div class="css_editable_mode_display">&nbsp;</div>' +
                            '<div class="media_iframe_video_size custom_video_size" contenteditable="false">&nbsp;</div>' +
                            '<video style="width:100%;" autoplay="autoplay" loop="loop" muted="muted" playsinline="playsinline" data-oe-expression="' + this.$content.attr('data-oe-expression') + '">' +
                            '<source src="' + this.$content.attr('data-oe-expression') + '"type="video/mp4"/>' + 
                            '</video><div class="video-progress d-none"><div class="video-progress-filled d-none"/></div>' +
                        '</div>'
                    );
                    this.media = this.$media[0];
                }   
            }
            else{
                if (this.$('.o_video_dialog_iframe').is('iframe')) {
                this.$media = $(
                    '<div class="media_iframe_video" data-oe-expression="' + this.$content.attr('src') + '">' +
                        '<div class="css_editable_mode_display">&nbsp;</div>' +
                        '<div class="media_iframe_video_size" contenteditable="false">&nbsp;</div>' +
                        '<iframe src="' + this.$content.attr('src') + '" frameborder="0" contenteditable="false" allowfullscreen="allowfullscreen"></iframe>' +
                    '</div>'
                );
                this.media = this.$media[0];
            }
            }

            console.log("===media==>>>", this.media);
            
            return Promise.resolve(this.media);
        },

        _getVideoURLData: function (url, options) {
            // if (!url.match(/^(http:\/\/|https:\/\/|www\.).*(\.mp4|\.mkv)$/i) {
            //     console.log("over here --------")
            //     return {
            //         error: true,
            //         message: 'The provided url is invalid',
            //     };
            // }

            if (url.endsWith('mp4') || url.endsWith('webm')) {
                return {type: 'cdn', embedURL: url};
            }
            return this._super(...arguments);
        },
        _createVideoNode: function (url, options) {
            console.log("_createVideoNode======>>", url);
            if (url.endsWith('mp4') || url.endsWith('webm')) {
                options = options || {};
                const videoData = this._getVideoURLData(url, options);
                // console.log("=====>>>", videoData);
                // if (videoData.error) {
                    // return {errorCode: 0};
                // }
                // if (!videoData.type) {
                    // return {errorCode: 1};
                // }

                // <video style="width:100%;" autoplay="autoplay" controls="controls" data-oe-expression="/upload_video_snippet/static/src/video/default.mp4">
                //     <source t-attf-src="/upload_video_snippet/static/src/video/default.mp4" type="video/mp4"/>
                //     Your browser does not support the video tag.
                // </video>
                const $source = $('<source>').attr('src', videoData.embedURL)
                const $video = $('<video>').width(1280).height(720)
                    .attr('style', 'width:100%')
                    .attr('autoplay', 'autoplay')
                    .attr('muted', 'muted')
                    .attr('loop', 'loop')
                    .attr('playsinline', 'playsinline')
                    // .attr('controls', 'controls')

                    .attr('data-oe-expression', videoData.embedURL)
                    .addClass('o_video_dialog_iframe')
                    .append($source);

                return {$video: $video, type: 'cdn'};
            }
            else{
                return this._super(...arguments);
            }
            

            
        },
    });

});

