from odoo import api, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def get_custom_report_notes(self, field, position):
        self.ensure_one()

        all_notes = self.env["custom_report_notes.note"].search(
            self._custom_report_notes_domain(field, position)
        )
        matching_notes = self.env["custom_report_notes.note"]

        for note in all_notes:

            if not note.stock_picking_domain:
                continue

            domain = note._parse_stock_picking_domain()

            if not domain:
                continue

            domain.append(("id", "=", self.id))

            if self.env['stock.picking'].search(domain, limit=1):
                matching_notes |= note

        return matching_notes

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

    @api.model
    def search_count(self, args):
        relation_tuples = self.env.context.get(
            "preview_custom_report_note_stock_picking_state_ids"
        )
        if relation_tuples:
            state_ids = [
                _id for relation_tuple in relation_tuples for _id in relation_tuple[2]
                if relation_tuple[2]
            ]
            if state_ids:
                args = args + self.env[
                    "custom_report_notes.note"
                ]._get_base_stock_picking_domain(state_ids)
        return super().search_count(args)
