/* global ace */
odoo.define('onnet_project_module.state_selection_widget_colour', function (require) {
"use strict";

var core = require('web.core');
var dialogs = require('web.view_dialogs');
var registry = require('web.field_registry');
var rel_fields = require('web.relational_fields');
var basicFields = require('web.basic_fields');
var _t = core._t;

var FieldStateSelectionWidgetColour = basicFields.StateSelectionWidget.extend({

 _prepareDropdownValues: function () {
        var self = this;
        var _data = [];
        var current_stage_id = self.recordData.stage_id && self.recordData.stage_id[0];
        var stage_data = {
            id: current_stage_id,
            legend_normal: this.recordData.legend_normal || undefined,
            legend_blocked : this.recordData.legend_blocked || undefined,
            legend_done: this.recordData.legend_done || undefined,
        };
        _.map(this.field.selection || [], function (selection_item) {
            var value = {
                'name': selection_item[0],
                'tooltip': selection_item[1],
            };
            if (selection_item[0] === 'normal') {
                value.state_name = stage_data.legend_normal ? stage_data.legend_normal : selection_item[1];
            } else if (selection_item[0] === 'done') {
                value.state_class = 'o_status_green';
                value.state_name = stage_data.legend_done ? stage_data.legend_done : selection_item[1];
            } else if (selection_item[0] === 'pending') {
                value.state_class = 'o_status_yellow';
                value.state_name = stage_data.legend_pending ? stage_data.legend_pending : selection_item[1];
            } else {
                value.state_class = 'o_status_red';
                value.state_name = stage_data.legend_blocked ? stage_data.legend_blocked : selection_item[1];
            }
            _data.push(value);
        });
        return _data;
    },


});

registry.add('state_selection_widget_colour', FieldStateSelectionWidgetColour);

return {
    FieldStateSelectionWidgetColour: FieldStateSelectionWidgetColour
};

});