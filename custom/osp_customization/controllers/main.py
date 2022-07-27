from odoo import http, SUPERUSER_ID, _
from odoo.http import route, request


class OspPopup(http.Controller):

    @route('/osp_customization/osp_popup/submit', type='json', website=True, auth="public")
    def osp_popup_submit(self, name, company_name, email, phone, medium, **post):
        if not request.env['ir.http']._verify_request_recaptcha_token('osp_popup_form'):
            return {
                'toast_type': 'danger',
                'toast_content': _("Suspicious activity detected by Google reCaptcha."),
            }
        Lead = request.env['crm.lead']
        lead_id = Lead.sudo().create({
            'medium_ref': medium,
            'contact_name': name,
            'partner_name': company_name,
            'name': name,
            'email_from': email,
            'phone': phone,
            'type': 'opportunity',
            'medium_id': request.env.ref('utm.utm_medium_website').sudo().id,
            'team_id': request.website.crm_default_team_id.id,
            'user_id': request.website.crm_default_user_id.id
        })
        visitor_sudo = request.env['website.visitor']._get_visitor_from_request()
        if visitor_sudo:
            if lead_id.sudo().exists():
                vals = {'lead_ids': [(4, lead_id.sudo().id)]}
                if not visitor_sudo.sudo().lead_ids and not visitor_sudo.partner_id:
                    vals['name'] = lead_id.sudo().contact_name
                visitor_sudo.write(vals)
        return True

    @http.route('/contactus', type='http', auth="public", website=True, sitemap=True)
    def contactus(self, **kw):
        values = request.env.context.copy()
        industries = request.env['osp.industry'].sudo().search([])
        values.update({
            'industries': industries
        })
        return request.render("website.contactus", values)
