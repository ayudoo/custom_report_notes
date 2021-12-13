# -*- coding: utf-8 -*-
from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def get_custom_report_notes(self, field, position):
        return self.env["custom_report_notes.note"].search(
            self._custom_report_notes_domain(field, position)
        )

    def _custom_report_notes_domain(self, field, position):
        domain = [
            ("field", "=", field),
            ("applicable_to_sale_orders", "=", True),
        ]
        if field != "bottom":
            domain.append(("position", "=", position))
        return domain
