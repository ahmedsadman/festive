import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


class Mailer:
    '''Send emails to a participant using SendGrid API'''
    def __init__(self):
        self.message = None

    def send_participation_mail(self, mail, identifier):
        self.message = Mail(
            from_email='ahmedsadman.211@gmail.com',
            to_emails=mail,
            subject='SendGrid ICT FEST',
            html_content='''<strong>Thanks for your participation</strong><br>
            Your team identifier is: <strong>{}</strong>'''.format(identifier)
        )
        self._send()

    def _send(self):
        try:
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(self.message)
            print(response.status_code)
            print(response.body)
        except Exception as e:
            print(e)

    