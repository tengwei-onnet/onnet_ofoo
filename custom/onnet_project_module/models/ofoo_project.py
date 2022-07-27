# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    legend_pending = fields.Char(
        'Yellow Kanban Label', default=lambda s: _('Pending Review'), translate=True, required=True,
        help='Override the default value displayed for the pending state for kanban selection, when the task or issue is in that stage.')


class Task(models.Model):
    _inherit = ["project.task"]

    teams = fields.Selection([('ofoo', 'OFOO'),
                              ('osim', 'OSIM'),
                              ('customer_service', 'CS'),
                              ('cloud_specialist', 'CLD')], required=True, store=True, default=None)
    user_phone_no = fields.Char(string="Phone Number", related='user_ids.phone_no', readonly=True)
    kanban_state = fields.Selection([
        ('normal', 'In Progress'),
        ('done', 'Ready'),
        ('blocked', 'Blocked'),
        ('pending', 'Pending Review')], string='Kanban State',
        copy=False, default='normal', required=True)
    legend_pending = fields.Char(related='stage_id.legend_pending', string='Kanban Pending Review Explanation', readonly=True, related_sudo=False)
    pending_review = fields.Boolean(string='Pending Review', default=False)

    def action_restore(self):
        self.pending_review = False
        self.color = None
        self.kanban_state = 'normal'

    def action_validate(self):
        self.pending_review = False
        self.color = None
        self.env['project.task'].search([('id', '=', self.id)]).write({'stage_id': 23})
        self.kanban_state = 'normal'

    def action_pending_review(self):
        self.color = 3
        self.pending_review = True
        self.kanban_state = 'pending'

    @api.depends('stage_id', 'kanban_state')
    def _compute_kanban_state_label(self):
        for task in self:
            if task.kanban_state == 'normal':
                task.color = None
                task.pending_review = False
                task.kanban_state_label = task.legend_normal
            elif task.kanban_state == 'blocked':
                task.color = None
                task.pending_review = False
                task.kanban_state_label = task.legend_blocked
            elif task.kanban_state == 'done':
                task.color = None
                task.pending_review = False
                task.kanban_state_label = task.legend_done
            elif task.kanban_state == 'pending':
                task.color = 3
                task.pending_review = True
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

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            teams = vals.get('teams')
            name = vals.get('name')
            standard_name = name.title()
            if teams:
                if teams == 'ofoo':
                    ofoo_id = self.env['ir.sequence'].next_by_code(
                        'onnet.ofoo')
                    if name is None:
                        vals['name'] = ofoo_id
                    vals['name'] = ofoo_id + ' ' + standard_name

                elif teams == 'osim':
                    osim_id = self.env['ir.sequence'].next_by_code(
                        'onnet.osim')
                    if name is None:
                        vals['name'] = osim_id
                    vals['name'] = osim_id + ' ' + standard_name

                elif teams == 'customer_service':
                    cs_id = self.env['ir.sequence'].next_by_code(
                        'onnet.cs')
                    if name is None:
                        vals['name'] = cs_id
                    vals['name'] = cs_id + ' ' + standard_name

                elif teams == 'cloud_specialist':
                    cld_id = self.env['ir.sequence'].next_by_code(
                        'onnet.cloud')
                    if name is None:
                        vals['name'] = cld_id
                    vals['name'] = cld_id + ' ' + standard_name

        res = super(Task, self).create(vals_list)
        return res

    def write(self, vals):
        if 'teams' in vals:
            new_team = vals['teams']
            old_team = self.teams
            if new_team != old_team:
                name = self.name
                split_name = str(name).split(" ", 1)
                if new_team == 'ofoo':
                    ofoo_id = self.env['ir.sequence'].next_by_code(
                        'onnet.ofoo')
                    vals['name'] = ofoo_id + ' ' + split_name[1]

                elif new_team == 'osim':
                    osim_id = self.env['ir.sequence'].next_by_code(
                        'onnet.osim')
                    vals['name'] = osim_id + ' ' + split_name[1]

                elif new_team == 'customer_service':
                    cs_id = self.env['ir.sequence'].next_by_code(
                        'onnet.cs')
                    vals['name'] = cs_id + ' ' + split_name[1]

                elif new_team == 'cloud_specialist':
                    cld_id = self.env['ir.sequence'].next_by_code(
                        'onnet.cloud')
                    vals['name'] = cld_id + ' ' + split_name[1]
        res = super(Task, self).write(vals)
        return res
