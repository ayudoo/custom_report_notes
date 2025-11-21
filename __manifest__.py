{
    "name": "Custom Report Notes",
    "summary": """
        Add some custom notes to your PDF reports""",
    "description": """
        Add some custom notes to your PDF reports.
    """,
    "author": "Michael Jurke, Ayudoo Ltd",
    "category": "Sales",
    "version": "0.1",
    "depends": [
        "base",
        "account",
        "sale",
        "stock",
    ],
    "data": [
        "security/notes_security.xml",
        "security/ir.model.access.csv",
        "views/note_view.xml",
        "views/res_config_settings_view.xml",
        "report/notes_block.xml",
        "report/report_deliveryslip.xml",
        "report/report_invoice.xml",
        "report/report_sale_order.xml",
        "report/report_templates.xml",
        "data/report_state_data.xml",
    ],
    "assets": {
        "web.report_assets_common": [
            "custom_report_notes/static/src/**/*",
        ],
    },
    "license": "LGPL-3",
    "application": True,
    "installable": True,
}
