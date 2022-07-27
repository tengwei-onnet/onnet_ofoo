odoo.define('osp_customization.osp_website', function (require) {
    'use strict';

    var ajax = require('web.ajax');
    const config = require('web.config');
    var dom = require('web.dom');
    var publicWidget = require('web.public.widget');
    var wUtils = require('website.utils');
    var animations = require('website.content.snippets.animation');

    const extraMenuUpdateCallbacks = [];
    var sAnimations = require('website.content.snippets.animation');
    sAnimations.registry.mediaVideo.include({
        start: function () {
            var videoSrc = this.$target.data('oe-expression')
            if (videoSrc){
                if (videoSrc.endsWith('mp4')) {
                    var $iframe_lenth = this.$target.find('iframe');
                    if ($iframe_lenth.length === 0) {
                        this.$target.append('<iframe style="display:none;"/>');
                    }
                }
            }
            return this._super(...arguments);
        }
    });

    $.fn.visibleHeight = function() {
        var elBottom, elTop, scrollBot, scrollTop, visibleBottom, visibleTop;
        scrollTop = $(window).scrollTop();
        scrollBot = scrollTop + $(window).height();
        elTop = this.offset().top;
        elBottom = elTop + this.outerHeight();
        visibleTop = elTop < scrollTop ? scrollTop : elTop;
        visibleBottom = elBottom > scrollBot ? scrollBot : elBottom;
        return visibleBottom - visibleTop
    }

    // Global call when document is ready
    $(function () {
        $('video').each(function () {
            $(this).attr('playsinline','playsinline');
        });

        $('.media_iframe_video').each(function () {
            var video_element = $(this).find('video')[0];
            var video_progress_bar = $(this).find('.video-progress');
            var video_progress = $(this).find('.video-progress').find('.video-progress-filled');
            video_progress_bar.removeClass('d-none');
            video_progress.removeClass('d-none');

            video_element.addEventListener('timeupdate', (event) => {
                if (video_progress.length > 0) {
                    var percentage = (video_element.currentTime / video_element.duration ) * 100;
                    video_progress[0].style.width = percentage + '%';
                }
            });
        });

        if ($('.editor_enable').length == 0){
            $('#wrapwrap').scroll(function() {
                var navbartop  = $("#top").offset().top + $("#top").height();
                var videos = document.getElementsByTagName("video");
                $('video').each(function() {
                    try {
                        if ($(this).visibleHeight() > 0){
                            $(this).attr('mute','mute');
                            $(this).attr('loop','loop');
                            if ( $(this)[0].readyState === 4 && $(this)[0].paused){
                                $(this).prop('muted', true);
                                var playPromise = $(this)[0].play();
                                // In browsers that don’t yet support this functionality,
                                // playPromise won’t be defined.
                                if (playPromise !== undefined) {
                                    playPromise.then(function() {
                                        // Automatic playback started!
                                    }).catch(function(error) {
                                        // Automatic playback failed.
                                        // Show a UI element to let the user manually start playback.
                                    });
                                }
                            }
                        }
                        else{
                            $(this).attr('mute','mute');
                            $(this).attr('loop','loop');
                            if ( $(this)[0].readyState === 4 && !$(this)[0].paused){
                                var playPromise = $(this)[0].pause();

                                // In browsers that don’t yet support this functionality,
                                // playPromise won’t be defined.
                                if (playPromise !== undefined) {
                                    playPromise.then(function() {
                                        // Automatic playback started!
                                    }).catch(function(error) {
                                        // Automatic playback failed.
                                        // Show a UI element to let the user manually start playback.
                                    });
                                }
                            }
                        }
                    }
                    catch(err) {
                      console.log("cant auto play")
                    }
                });
            });
        }
    });
});