odoo.define('osp_customization.s_website_form', function (require) {
    'use strict';

    var core = require('web.core');
    var publicWidget = require('web.public.widget');

    var _t = core._t;
    var qweb = core.qweb;

    publicWidget.registry.s_website_form.include({
        start: function () {
            // Initialize IntlTelInput
            var phone_input = document.querySelector(".intlTelInput");
            if (phone_input) {
                this.itiPhone = window.intlTelInput(phone_input, {
                    separateDialCode: true,
                    preferredCountries: ['my', 'in', 'us'],
                    utilsScript: "/intl_phone_field/static/src/lib/utils.js",
                });
            }
            return this._super(...arguments).then(() => this.__startResolve());
        },

       check_error_fields: function (error_fields) {
//            var res = this._super.apply(this, arguments);
            if ($('input.intlTelInput').length) {
                    var fullNumber = this.itiPhone.getNumber();
                    $('input.intlTelInput').val(fullNumber);
            }
            return true;
        },

//        check_error_fields: function (error_fields) {
//            var res = this._super.apply(this, arguments);
//            if (res && $("input[type=email]").length) {
//                var emailField = $("input[type=email]");
//                var mailformat = new RegExp("^(([^<>()[\\]\\\\.,;:\\s@\"]+(\\.[^<>()[\\]\\\\.,;:\\s@\"]+)*)|(\".+\"))@((\\[[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\])|(([a-zA-Z\\-0-9]+\\.)+[a-zA-Z]{2,}))$");
//                if (!mailformat.test(emailField.val())) {
//                    this.update_status('error', _t("Please enter a valid email address."));
//                    emailField.addClass('is-invalid');
//                    return false;
//                } else {
//                    emailField.removeClass('is-invalid');
//                }
//            }
//            return res
//        },

        update_status: function (status, message) {
            var module = document.getElementById("submit_invalid").innerHTML = "An error occurred, please try again later. ";
            var res = this._super.apply(this, arguments);
            if (status == 'error'){
                $("#submit_invalid").show();
            }
        },
    });
});
