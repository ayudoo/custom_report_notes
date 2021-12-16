# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ReportState(models.Model):
    _name = "custom_report_notes.report_state"
    _description = "Report State"
    _order = "sequence,id"

    sequence = fields.Integer("Sequence")

    name = fields.Char(
        string="Name",
        required=True,
        index=True,
        translate=True,
    )

    res_model = fields.Selection(
        [
            ("sale.order", "Sales Order"),
            ("stock.picking", "Stock Picking"),
            ("account.move", "Account Move"),
        ],
        string="Report Type",
        required=True,
    )
