from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools import config as odoo_conf

PROJECT_STATUS = [
    ("Unconfirmed", "Не подтверждён"),
    ("OnApproval", "На утверждении"),
    ("TeamFormation", "Формирование команды"),
    ("Teamwork", "Работа команды"),
    ("Ready to defend", "Готовы к защите"),
    ("Past", "C оценкой")
]

status_with_stage_id = {
    int(odoo_conf['project_stage_1_id']): "Unconfirmed",
    int(odoo_conf['project_stage_2_id']): "OnApproval",
    int(odoo_conf['project_stage_3_id']): "TeamFormation",
    int(odoo_conf['project_stage_4_id']): "Teamwork",
    int(odoo_conf['project_stage_5_id']): "Ready to defend",
    int(odoo_conf['project_stage_6_id']): "Past",
}


class LpProject(models.Model):
    _name = 'lp.project'
    _inherit = ['mail.thread']
    _description = 'Project D'

    # Project info
    name = fields.Char(string="Название проекта", tracking=True, required=True)
    short_description = fields.Text(string="Описание проекта", tracking=True)
    description = fields.Text(string="Необходимые участники команды (Пример: backend, 2 frontend, ML)", tracking=True)
    logo = fields.Image(string="Project logo")

    status = fields.Selection(PROJECT_STATUS, string="Статус", readonly=True, tracking=True, default="Unconfirmed")
    author = fields.Many2one('res.partner', string="Автор", compute='compute_author', readonly=True, tracking=True)

    project_info = fields.Many2many('ir.attachment', 'lp_project_info_document_ir_attachments_rel',
                                    'lp_project_id', 'attachment_id', 'Project info', tracking=True, copy=True)

    # Accept Project info by lecturer
    confirmed_id = fields.Many2one('res.partner', string="Подтверждено", readonly=True, tracking=True)

    # project
    project = fields.Many2one('project.project', string="Канбан", readonly=True, tracking=True)
    stage_id = fields.Many2one(related='project.stage_id', string="Статус", readonly=True, tracking=True)
    tag_ids = fields.Many2many(related='project.tag_ids', string="Навыки", tracking=True)

    # Team
    message_partner_ids = fields.Many2many(related='project.message_partner_ids', string="message_follower_ids", readonly=True, tracking=True)
    max_col_users = fields.Integer(string="Максимальное количество учасников", default=5, readonly=True, tracking=True)
    current_value_users = fields.Integer(string="Текущее количество учасников", default=0, readonly=True, tracking=True)

    @api.depends('max_col_users', 'current_value_users')
    def _compute_is_all_invited(self):
        for record in self:
            record.is_all_invited = record.current_value_users >= record.max_col_users

    is_all_invited = fields.Boolean('Is All invited', compute='_compute_is_all_invited', store=True, readonly=True, tracking=True)

    # Invitation Bachelor
    invitation_bachelor_ids = fields.One2many('lp.invitation.bachelor', 'project_id', domain=[('invited_status', '!=', 'draft')], string='Project info', readonly=True, tracking=True)

    @api.model
    def create(self, vals):
        self.validate_count_creations()
        return super(LpProject, self).create(vals)

    def write(self, vals):
        if vals.get("status") != status_with_stage_id.get(self.stage_id):
            vals.update(self.change_status_to_stage_id_event(vals.get("status")))
        return super(LpProject, self).write(vals)

    def validate_count_creations(self):
        project = self.env['lp.project'].search([('create_uid', '=', self.env.uid)])
        if len(project) > 0:
            raise ValidationError("Магистр может создать только 1 проект")

    @api.depends('author')
    def compute_author(self):
        for rec in self:
            author = self.env['res.users'].browse(rec.create_uid.id).partner_id
            rec.author = author.id

    def send_confirm_project(self):
        if not self.project:
            project = self.env['project.project'].create({
                'name': self.name,
                'stage_id': int(odoo_conf['project_stage_2_id'])
            })
            project.write({'message_partner_ids': [(4, self.author.id)]})

            self.write({'project': project.id, 'status': 'OnApproval'})
        else:
            self.write({'status': 'OnApproval'})

    def confirm_project(self):
        partner = self.env['res.users'].browse(self.env.uid).partner_id
        return self.write({'status': 'TeamFormation',
                           'confirmed_id': partner.id})

    def action_view_tasks(self):
        project_id = self.project.id
        return self.project.action_custom_view_tasks(project_id)

    def change_status_to_stage_id_event(self, status):
        if status is None:
            return {}
        status_with_stage_id = {
            "Unconfirmed": int(odoo_conf['project_stage_1_id']),
            "OnApproval": int(odoo_conf['project_stage_2_id']),
            "TeamFormation": int(odoo_conf['project_stage_3_id']),
            "Teamwork": int(odoo_conf['project_stage_4_id']),
            "Ready to defend": int(odoo_conf['project_stage_5_id']),
            "Past": int(odoo_conf['project_stage_6_id']),
        }

        if status_with_stage_id.get(status) is None:
            raise ValidationError("Сообщите в айти отдел")

        return {"stage_id": status_with_stage_id.get(status)}

    def change_stage_id_to_status_event(self, ):
        if self.stage_id is None:
            return {}
        if status_with_stage_id.get(self.stage_id) is None:
            raise ValidationError("Сообщите в айти отдел stage_id")

        self.write({'status': status_with_stage_id.get(stage_id)})
