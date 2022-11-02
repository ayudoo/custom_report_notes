from odoo import api, fields, models


class CustomReportNote(models.Model):
    _name = "custom_report_notes.note"
    _description = "Custom Report Note"
    _order = "sequence,id"

    sequence = fields.Integer("Sequence")

    active = fields.Boolean(default=True)

    name = fields.Char(
        string="Name",
        required=True,
        index=True,
        translate=True,
    )

    field = fields.Selection(
        [
            ("address", "Address"),
            ("heading", "Heading"),
            ("table", "Table"),
            ("signature_comment", "Signature/Comment"),
            ("bottom", "Bottom"),
        ],
        default="signature_comment",
        required=True,
    )

    position = fields.Selection(
        [
            ("before", "Before"),
            ("after", "After"),
        ],
        default="after",
        required=True,
    )

    applicable_to_sale_orders = fields.Boolean(
        "Applicable To Sales Orders",
        default=True,
    )
    sale_order_state_ids = fields.Many2many(
        string="Sales Order States",
        comodel_name="custom_report_notes.report_state",
        relation="custom_report_notes_note_sale_order_state_rel",
        domain=[('res_model', '=', 'sale.order')],
    )
    applicable_to_stock_pickings = fields.Boolean(
        "Applicable To Deliveries",
        default=True,
    )
    stock_picking_state_ids = fields.Many2many(
        string="Delivery States",
        comodel_name="custom_report_notes.report_state",
        relation="custom_report_notes_note_stock_picking_state_rel",
        domain=[('res_model', '=', 'stock.picking')],
    )
    applicable_to_account_moves = fields.Boolean(
        "Applicable To Invoices",
        default=True,
    )
    account_move_state_ids = fields.Many2many(
        string="Invoice States",
        comodel_name="custom_report_notes.report_state",
        relation="custom_report_notes_note_account_move_state_rel",
        domain=[('res_model', '=', 'account.move')],
    )

    content = fields.Html("Content", translate=True, required=True)

    def _get_combinations(self):
        positions = list(
            dict(self._fields["position"]._description_selection(self.env)).values()
        )
        fields_dict = dict(self._fields["field"]._description_selection(self.env))
        combinations = []

        for key, field in fields_dict.items():
            if key == "bottom":
                combinations.append(field)
            else:
                for position in positions:
                    combinations.append(" ".join([position, field]))
        return combinations

    def _get_position_label(self):
        value = None
        if self.position:
            value = dict(self._fields["position"]._description_selection(self.env)).get(
                self.position
            )
        return value

    def _get_field_label(self):
        value = None
        if self.field:
            value = dict(self._fields["field"]._description_selection(self.env)).get(
                self.field
            )
        return value

    def _get_default_name(self):
        if self.field == "bottom":
            return self._get_field_label()
        else:
            return " ".join([self._get_position_label(), self._get_field_label()])

    @api.onchange("field", "position")
    def onchange_field_or_position(self):
        if not self.name or self.name in self._get_combinations():
            self.name = self._get_default_name()
