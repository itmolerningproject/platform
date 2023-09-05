from datetime import date
from odoo import fields, models


class CrmLeadLost(models.TransientModel):
    _name = 'crm.lead.lost'
    _description = 'Get Lost Reason'

    lost_reason_id = fields.Many2one('crm.lost.reason', 'Lost Reason')
    note =

    def assign_claim(self):


