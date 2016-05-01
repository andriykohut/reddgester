import os
import smtplib

from email.mime.text import MIMEText

from nameko.rpc import rpc
from jinja2 import Environment
from jinja2 import FileSystemLoader

TEMPLATE = Environment(
    loader=FileSystemLoader('./templates/')
).get_template('digest.jinja2')


class Mailer(object):
    name = "mailer"

    @rpc
    def send_digest(self, context, to):
        message = TEMPLATE.render(context)
        msg = MIMEText(message, 'html')
        msg['Subject'] = "Top {} from /r/{}".format(
            context['limit'], context['r'])
        msg['From'] = os.getenv('DIGEST_FROM', 'andriy.kogut@gmail.com')
        msg['To'] = to
        smtp = smtplib.SMTP(
            os.getenv('SMTP_HOST', 'localhost'),
            os.getenv('SMTP_PORT', 25))
        smtp.send_message(msg)
        smtp.quit()
