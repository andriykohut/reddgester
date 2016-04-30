import os
import smtplib

from email.mime.text import MIMEText

from nameko.rpc import rpc


class Mailer(object):
    name = "mailer"

    @rpc
    def send_digest(self, digest, to):
        msg = MIMEText(digest)
        msg['Subject'] = digest['subject']
        msg['From'] = os.getenv('DIGEST_FROM', 'andriy.kogut@gmail.com')
        msg['To'] = to
        smtp = smtplib.SMTP(
            os.getenv('SMTP_HOST', 'localhost'),
            os.getenv('SMTP_PORT', 25))
        smtp.send_message(msg)
        smtp.quit()
