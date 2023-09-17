import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)

ACADEMIC_DEGREE = [
    ("bachelor", 'Бакалавр'),
    ("master", 'Магистрант'),
    ("aspirant", 'Аспирант'),
]

FULL_FIO_TEMPLATE = "{last_name} {name} {surname}"


class Partner(models.Model):
    _inherit = 'res.partner'
    _description = "Partner"
    _order = 'write_date desc'

    name = fields.Char(string='ФИО', tracking=True)
    firstname = fields.Char(string='Firstname', tracking=True)
    lastname = fields.Char(string='Lastname', tracking=True)

    #todo Сипаретк ФИО
    #todo hide others filds in viivs
    #todo Сделать доступ к эти поля чере import  academic_degree, number_groups

    academic_degree = fields.Selection(ACADEMIC_DEGREE, "Академическая степень")
    ear = fields.Char("Год", tracking=True)
    number_groups = fields.Char("Группа", tracking=True)
    category_id = fields.Many2many('res.partner.category', string='Skill Stack', tracking=True)

    #
    in_project = fields.Boolean("В проекте", tracking=True)
    lp_project_id = fields.Many2one('lp.project', string="Проект", readonly=True)


    # roles
    is_admin = fields.Boolean(compute='_compute_get_is_admin')
    is_master = fields.Boolean(compute='_compute_get_is_master')
    is_bachelor = fields.Boolean(compute='_compute_get_is_bachelor')
    is_lecturer = fields.Boolean(compute='_compute_get_is_lecturer')


    def _compute_get_is_admin(self):
        for rec in self:
            user = self.env['res.users'].search([('partner_id', '=', rec.id)], limit=1)
            group_external_ids = user.get_group_external_ids()
            rec.is_admin = False
            if 'Admin' in group_external_ids:
                rec.is_admin = True

    def _compute_get_is_master(self):
        for rec in self:
            user = self.env['res.users'].search([('partner_id', '=', rec.id)], limit=1)
            group_external_ids = user.get_group_external_ids()
            rec.is_master = False
            if 'Master' in group_external_ids:
                rec.is_master = True
    def _compute_get_is_bachelor(self):
        for rec in self:
            user = self.env['res.users'].search([('partner_id', '=', rec.id)], limit=1)
            group_external_ids = user.get_group_external_ids()
            rec.is_bachelor = False
            if 'Bachelor' in group_external_ids:
                rec.is_bachelor = True
    def _compute_get_is_lecturer(self):
        for rec in self:
            user = self.env['res.users'].search([('partner_id', '=', rec.id)], limit=1)
            group_external_ids = user.get_group_external_ids()
            rec.is_lecturer = False
            if 'Lecturer' in group_external_ids:
                rec.is_lecturer = True

    @api.model
    def create(self, vals):
        return super(Partner, self).create(vals)

    def write(self, vals):
        return super(Partner, self).write(vals)
