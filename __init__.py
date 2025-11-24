import os
from odoo import modules, tools

from . import models


def _post_init_hook(env):
    pathname = os.path.join(modules.get_module_path('custom_report_notes'), 'report', 'din5008_report.xml')
    with tools.file_open(pathname, 'rb') as fp:
        tools.convert.convert_xml_import(env, 'custom_report_notes', fp)
