# This file is part of csv_import_send_mail module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta

__all__ = ['Template']
__metaclass__ = PoolMeta


class Template:
    __name__ = 'electronic.mail.template'

    csv_import = fields.Boolean('Allow CSV imports',
        help=('Check this box to allow send emails from csv_import module for '
            'each record imported.'))
