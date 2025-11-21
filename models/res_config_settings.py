from odoo import models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    def action_custom_report_notes(self):
        return {
            "view_mode": "list",
            "view_id": self.env.ref(
                "custom_report_notes.view_custom_report_note_tree"
            ).id,
            "res_model": "ssol_hogast.connector",
            "type": "ir.actions.act_window",
            "target": "new",
        }
