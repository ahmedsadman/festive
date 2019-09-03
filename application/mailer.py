import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


class Mailer:
    '''Send emails to a participant using SendGrid API'''

    def __init__(self):
        self.message = {
            'personalizations': [
                {
                    'to': [
                        {
                            'email': None
                        }
                    ],
                    'subject': 'Confirmation of participation'
                }
            ],
            'from': {
                'email': 'ahmedsadman.211@gmail.com',
                'name': 'ICT Fest 2020'
            },
            'content': [
                {
                    'type': 'text/html',
                    'value': None
                }
            ]
        }

    def _set_email(self, email):
        self.message['personalizations'][0]['to'][0]['email'] = email

    def _set_html_content(self, content):
        self.message['content'][0]['value'] = content

    def send_participation_mail(self, email, identifier):
        html_content = '''<strong>Thanks for your participation</strong><br>
            Your team identifier is: <strong>{}</strong>'''.format(identifier)
        self._set_email(email)
        self._set_html_content(html_content)
        self._send()

    def _send(self):
        try:
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(self.message)
            print(response.status_code)
            print(response.body)
        except Exception as e:
            print(e)
