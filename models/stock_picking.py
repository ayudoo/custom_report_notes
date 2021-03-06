# -*- coding: utf-8 -*-
from odoo import models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def get_custom_report_notes(self, field, position):
        return self.env["custom_report_notes.note"].search(
            self._custom_report_notes_domain(field, position)
        )

    def _custom_report_notes_domain(self, field, position):
        domain = [
            ("field", "=", field),
            ("applicable_to_stock_pickings", "=", True),
            ("|"),
            ("stock_picking_state_ids", "=", False),
            ("stock_picking_state_ids.id", "=", self._custom_report_notes_state()),
        ]
        if field != "bottom":
            domain.append(("position", "=", position))
        return domain

    def _custom_report_notes_state(self):
        return self.env.ref("custom_report_notes.stock_picking_state_{}".format(
            self.state
        )).id
