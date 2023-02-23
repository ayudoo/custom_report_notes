import logging
from ast import literal_eval
from odoo import api, fields, models

_logger = logging.getLogger(__name__)


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

    page_break = fields.Boolean("Page Break", default=False)

    content = fields.Html("Content", translate=True, required=True)

    # Sales Order Filters

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

    @api.model
    def _get_base_sale_order_domain(self, state_ids):
        states = self.env["custom_report_notes.report_state"].browse(state_ids)
        domain = [("state", "in", states.with_context(lang=False).mapped('name'))]
        return domain

    def _get_default_sale_order_domain(self):
        return []

    def _compute_sale_order_domain(self):
        for record in self:
            record.sale_order_domain = repr(record._get_default_sale_order_domain())

    def _parse_sale_order_domain(self):
        self.ensure_one()
        try:
            domain = literal_eval(self.sale_order_domain)
        except Exception as e:
            _logger.warning(
                "Invalid sale.order domain for report note #{}: {}".format(
                    self.id, str(e)
                )
            )
            domain = []
        return domain

    sale_order_domain = fields.Char(
        string="Sales Order Domain",
        compute=_compute_sale_order_domain,
        readonly=False,
        store=True,
    )

    # Stock Picking Filters

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

    @api.model
    def _get_base_stock_picking_domain(self, state_ids):
        states = self.env["custom_report_notes.report_state"].browse(state_ids)
        domain = [("state", "in", states.with_context(lang=False).mapped('name'))]
        return domain

    def _get_default_stock_picking_domain(self):
        return []

    def _compute_stock_picking_domain(self):
        for record in self:
            record.stock_picking_domain = repr(
                record._get_default_stock_picking_domain()
            )

    def _parse_stock_picking_domain(self):
        self.ensure_one()
        try:
            domain = literal_eval(self.stock_picking_domain)
        except Exception as e:
            _logger.warning(
                "Invalid stock.picking domain for report note #{}: {}".format(
                    self.id, str(e)
                )
            )
            domain = []
        return domain

    stock_picking_domain = fields.Char(
        string="Stock Picking Domain",
        compute=_compute_stock_picking_domain,
        readonly=False,
        store=True,
    )

    # Account Moves Filters

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

    @api.model
    def _get_base_account_move_domain(self, state_ids):
        states = self.env["custom_report_notes.report_state"].browse(state_ids)
        domain = [("state", "in", states.with_context(lang=False).mapped('name'))]
        return domain

    def _get_default_account_move_domain(self):
        return []

    def _compute_account_move_domain(self):
        for record in self:
            record.account_move_domain = repr(
                record._get_default_account_move_domain()
            )

    def _parse_account_move_domain(self):
        self.ensure_one()
        try:
            domain = literal_eval(self.account_move_domain)
        except Exception as e:
            _logger.warning(
                "Invalid account.move domain for report note #{}: {}".format(
                    self.id, str(e)
                )
            )
            domain = []
        return domain

    account_move_domain = fields.Char(
        string="Account Move Domain",
        compute=_compute_account_move_domain,
        readonly=False,
        store=True,
    )

    # helper methods

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
