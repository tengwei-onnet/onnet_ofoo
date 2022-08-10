# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    legend_pending = fields.Char(
        'Yellow Kanban Label', default=lambda s: _('Pending Review'), translate=True, required=True,
        help='Override the default value displayed for the pending state for kanban selection, when the task or issue is in that stage.')


# class ProjectTeam(models.Model):
#     _name = "project.team"
#     _description = "Project Team"
#
#     name = fields.Char(string='Team', store=True)
#     task_id = fields.One2many(comodel_name='project.task', inverse_name='team_id', readonly=True)
#     count_task = fields.Integer(string='Tasks Count', compute='count_team_task')
#
#     @api.depends('task_id')
#     def count_team_task(self):
#         for rec in self:
#             rec.count_task = len(self.task_id)
#
#     _sql_constraints = [
#         ('unique_category_name', 'unique(name)', 'Name must be unique')
#     ]
#
#     def action_view_task(self):
#         return {
#             'name': 'Team Task',
#             'res_model': 'project.task',
#             'view_mode': 'list,form,kanban',
#             'context': {'default_team_id': self.id},
#             'domain': [('team_id', '=', self.id)],
#             'target': 'current',
#             'type': 'ir.actions.act_window',
#         }


class Task(models.Model):
    _inherit = 'project.task'

    team_id = fields.Many2one(comodel_name='helpdesk.team', string='Team', store=True, tracking=True, default=None, required=True)
    user_phone_no = fields.Char(string="Phone Number", related='user_ids.phone_no', readonly=True)
    team_name = fields.Char(string='Team Name', related='team_id.name', readonly=True, store=True)
    kanban_state = fields.Selection([
        ('normal', 'In Progress'),
        ('done', 'Ready'),
        ('blocked', 'Blocked'),
        ('pending', 'Pending Review')], string='Kanban State',
        copy=False, default='normal', required=True)
    legend_pending = fields.Char(related='stage_id.legend_pending', string='Kanban Pending Review Explanation',
                                 readonly=True, related_sudo=False)
    sequence_id = fields.Char(string='Sequence Code', related='team_id.sequence_id', readonly=True)

    @api.depends('stage_id', 'kanban_state')
    def _compute_kanban_state_label(self):
        for task in self:
            if task.kanban_state == 'normal':
                task.kanban_state_label = task.legend_normal
            elif task.kanban_state == 'blocked':
                task.kanban_state_label = task.legend_blocked
            elif task.kanban_state == 'done':
                task.kanban_state_label = task.legend_done
            else:
                task.kanban_state_label = task.legend_pending

    def action_send_whatsapp(self):
        # Store user_ids name in array list
        array_name = []
        for rec in self.user_ids:
            array_name.append(rec.name)

        if not self.user_phone_no:
            raise ValidationError("Missing phone number in this record")

        new_str = self.user_phone_no
        valid_phone_no = new_str.replace("-", "")

        # Need to convert Hashtag # to ASCII code in url link
        task_title = self.name
        valid_task_title = task_title.replace("#", "%23")

        # convert date format to string
        if not self.date_deadline:
            date_deadline = ' '
        else:
            date_deadline = str(self.date_deadline)

        msg = "Task Title:%09*" + valid_task_title + "*%0aAssigned To:%09" + (", ".join(array_name)) + "%0aDeadline:%09%09" + \
              date_deadline + "%0aMessage:%09"

        whatsapp_url = 'https://api.whatsapp.com/send?phone=+6' + valid_phone_no + '&text=' + msg

        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': whatsapp_url
        }

    # Add a new team, need to add another if else for the new team
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            sequence = vals.get('sequence_id')
            name = vals.get('name')
            standard_name = name.title()

            if sequence:
                task_id = self.env['ir.sequence'].next_by_code(sequence)
                vals['name'] = task_id + ' ' + standard_name
            elif not self.env['ir.sequence'].next_by_code(sequence):
                vals['name'] = standard_name

        res = super(Task, self).create(vals_list)
        return res

            # teams = vals.get('team_name')
            # name = vals.get('name')
            # standard_name = name.title()
            # if teams:
            #     if teams == 'OFOO':
            #         ofoo_id = self.env['ir.sequence'].next_by_code(
            #             'onnet.ofoo')
            #         if name is None:
            #             vals['name'] = ofoo_id
            #         vals['name'] = ofoo_id + ' ' + standard_name
            #
            #     elif teams == 'OSIM':
            #         osim_id = self.env['ir.sequence'].next_by_code(
            #             'onnet.osim')
            #         if name is None:
            #             vals['name'] = osim_id
            #         vals['name'] = osim_id + ' ' + standard_name
            #
            #     elif teams == 'Customer Service':
            #         cs_id = self.env['ir.sequence'].next_by_code(
            #             'onnet.cs')
            #         if name is None:
            #             vals['name'] = cs_id
            #         vals['name'] = cs_id + ' ' + standard_name
            #
            #     elif teams == 'Cloud Specialist':
            #         cld_id = self.env['ir.sequence'].next_by_code(
            #             'onnet.cloud')
            #         if name is None:
            #             vals['name'] = cld_id
            #         vals['name'] = cld_id + ' ' + standard_name
            #     else:
            #         vals['name'] = 'undefined_team' + ' ' + standard_name

        res = super(Task, self).create(vals_list)
        return res

    def write(self, vals):
        if 'sequence_id' in vals:
            new_sequence_id = vals['sequence_id']
            old_sequence_id = self.sequence_id
            name = self.name
            if new_sequence_id != old_sequence_id:
                if old_sequence_id is False:
                    task_id = self.env['ir.sequence'].next_by_code(new_sequence_id)
                    vals['name'] = task_id + ' ' + name
                else:
                    split_name = str(name).split(" ", 1)
                    task_id = self.env['ir.sequence'].next_by_code(new_sequence_id)
                    vals['name'] = task_id + ' ' + split_name[1]


        # if 'team_name' in vals:
        #     new_team = vals['team_name']
        #     old_team = self.team_name
        #     if new_team != old_team:
        #         name = self.name
        #         split_name = str(name).split(" ", 1)
        #         if new_team == 'OFOO':
        #             ofoo_id = self.env['ir.sequence'].next_by_code(
        #                 'onnet.ofoo')
        #             vals['name'] = ofoo_id + ' ' + split_name[1]
        #
        #         elif new_team == 'OSIM':
        #             osim_id = self.env['ir.sequence'].next_by_code(
        #                 'onnet.osim')
        #             vals['name'] = osim_id + ' ' + split_name[1]
        #
        #         elif new_team == 'Customer Service':
        #             cs_id = self.env['ir.sequence'].next_by_code(
        #                 'onnet.cs')
        #             vals['name'] = cs_id + ' ' + split_name[1]
        #
        #         elif new_team == 'Cloud Specialist':
        #             cld_id = self.env['ir.sequence'].next_by_code(
        #                 'onnet.cloud')
        #             vals['name'] = cld_id + ' ' + split_name[1]
        #         else:
        #             vals['name'] = 'undefined_team' + ' ' + split_name[1]

        res = super(Task, self).write(vals)
        return res
