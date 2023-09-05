import requests
from datetime import datetime, timedelta
from odoo import api, models
from odoo.tools import config as odoo_conf


class IrActionsServer(models.Model):
    _inherit = "ir.actions.server"

    @api.model
    def _get_eval_context(self, action=None):
        self.env.context = dict(self.env.context)
        self.env.context.update({
            # 'garentii_user_jwt': odoo_conf['garentii_user_jwt'],
            # 'garentii_user_id': odoo_conf['garentii_user_id'],
            # 'garentii_api_uri': odoo_conf['garentii_api_uri'],
            # 'garentii_odoo_url': odoo_conf['garentii_odoo_url'],
            # 'odoo_domain_name': odoo_conf['odoo_domain_name'],
            "project_stage_1_id": int(odoo_conf['project_stage_1_id']),
            "project_stage_2_id": int(odoo_conf['project_stage_2_id']),
            "project_stage_3_id": int(odoo_conf['project_stage_3_id']),
            "project_stage_4_id": int(odoo_conf['project_stage_4_id']),
            "project_stage_5_id": int(odoo_conf['project_stage_5_id']),
            "project_stage_6_id": int(odoo_conf['project_stage_6_id']),
        })
        eval_context = super(IrActionsServer, self)._get_eval_context(action)

        def make_request(*args, **kwargs):
            return requests.request(*args, **kwargs)

        eval_context["datetime"] = datetime
        eval_context["timedelta"] = timedelta
        eval_context["make_request"] = make_request

        return eval_context

    @api.model
    def run_by_record(self, record):
        res = False
        for action in self.sudo():
            eval_context = self._get_eval_context(action=action)
            eval_context.update({
                'record': record
            })

            runner, multi = action._get_runner()
            run_self = action.with_context(active_ids=[record.id], active_id=record.id)
            res = runner(run_self, eval_context=eval_context)

        return res or False
