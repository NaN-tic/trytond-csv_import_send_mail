# This file is part of csv_import_send_mail module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool, PoolMeta

__all__ = ['CSVArchive']
__metaclass__ = PoolMeta


class CSVArchive:
    __name__ = 'csv.archive'

    @classmethod
    def post_import(cls, model, records):
        pool = Pool()
        Email = pool.get('electronic.mail')
        Template = pool.get('electronic.mail.template')
        templates = Template.search([
                ('model', '=', model.id),
                ('csv_import', '=', True),
                ])
        if templates:
            template = templates[0]
            for record in records:
                email_message = Template.render(template, record)
                email = Email.create_from_email(
                    email_message, template.mailbox.id)
                Template.send_email(email, template)
                Template.add_event(template, record, email, email_message)
        super(CSVArchive, cls).post_import(model, records)
