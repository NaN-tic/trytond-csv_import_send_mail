# This file is part of csv_import_send_mail module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool, PoolMeta
from trytond.model import fields
from trytond.pyson import Eval
from trytond.config import config
from trytond.tools import get_smtp_server
from email.mime.text import MIMEText
from email.header import Header

import logging

__all__ = ['CSVProfile', 'CSVArchive']
__metaclass__ = PoolMeta


class CSVProfile:
    __name__ = 'csv.profile'
    send_email_group = fields.Boolean('Send Email Group')
    email_group = fields.Many2One('res.group', 'Email Group',
        states={
            'required': Eval('send_email_group', True),
        })
    send_email_template = fields.Boolean('Send Email Template')
    email_template = fields.Many2One('electronic.mail.template', 'Email Template',
        states={
            'required': Eval('send_email_template', True),
        })


class CSVArchive:
    __name__ = 'csv.archive'

    @classmethod
    def __setup__(cls):
        super(CSVArchive, cls).__setup__()
        cls._error_messages.update({
                'request_title': ('CSV Import %s successfully'),
                'request_body': ("CSV Import records: %s"),
                })

    @classmethod
    def post_import(cls, profile, records):
        pool = Pool()
        EmailConfiguration = pool.get('electronic.mail.configuration')

        #send email all users in profile group
        if profile.send_email_group:
            User = pool.get('res.user')

            subject = cls.raise_user_error('request_title',
                profile.model.name, raise_exception=False)
            body = cls.raise_user_error('request_body',
                ', '.join(map(str, records)), raise_exception=False)

            from_addr = config.get('email', 'from')
            users = User.search([
                ('groups', 'in', [profile.email_group.id]),
                ('active', '=', True),
                ('email', '!=', ''),
                ])
            if users:
                emails = [u.email for u in users]
                to_addr = ",".join(emails)
                msg = MIMEText(body, _charset='utf-8')
                msg['To'] = to_addr
                msg['From'] = from_addr
                msg['Subject'] = Header(subject, 'utf-8')

                try:
                    server = get_smtp_server()
                    server.sendmail(from_addr, to_addr, msg.as_string())
                    server.quit()
                except Exception, exception:
                    logger = logging.getLogger(__name__)
                    logger.error('Unable to deliver email (%s):\n %s'
                        % (exception, msg.as_string()))

        #render and send email from electronic mail template
        if profile.send_email_template and profile.email_template:
            Email = pool.get('electronic.mail')
            Template = pool.get('electronic.mail.template')
            email_configuration = EmailConfiguration(1)
            draft_mailbox = email_configuration.draft
            template = profile.email_template

            if template.queue:
                mailbox = template.mailbox_outbox \
                    if template.mailbox_outbox else email_configuration.outbox
            else:
                mailbox = template.mailbox if template.mailbox \
                    else email_configuration.sent
            mailbox = email_configuration.outbox

            electronic_emails = set()
            for record in records:
                rec = pool.get(profile.model.model)(record)
                email_message = template.render(rec)
                electronic_email = Email.create_from_email(
                    email_message, mailbox)
                template.add_event(rec, electronic_email)
                electronic_emails.add(electronic_email)

            if not template.queue:
                for electronic_mail in electronic_emails:
                    success = electronic_email.send_email()
                    if success:
                        logging.getLogger('Mail').info('Send email: %s' %
                            (electronic_email.rec_name))
                    else:
                        electronic_email.mailbox = draft_mailbox
                        electronic_email.save()

        super(CSVArchive, cls).post_import(profile, records)
