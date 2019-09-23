import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


class Mailer:
    """Send emails to a participant using SendGrid API"""

    def __init__(self):
        self.message = {
            "personalizations": [{"to": [{"email": None}], "subject": None}],
            "from": {
                "email": "ahmedsadman.211@gmail.com",
                "name": "ICT Fest 2020",
            },
            "content": [{"type": "text/html", "value": None}],
        }

    def _set_email(self, email):
        self.message["personalizations"][0]["to"][0]["email"] = email

    def _set_html_content(self, content):
        self.message["content"][0]["value"] = content

    def _set_subject(self, subject):
        self.message["personalizations"][0]["subject"] = subject

    def send_participation_mail(self, email, event, identifier):
        html_content = """
        Hello,<br>
        Thank you for participating in {event_name}. Your identifier is: \
        <strong>{identifier}</strong>. This will be required to verify \
        your payment. Please don't share the identifier with anyone.<br>
        Please proceed to <a href="https://www.google.com">payment</a> \
        to confirm your participation.<br>
        Looking forward to see you at the event.<br><br>
        <em>Regards,<br>
        IT Team, ICT Fest 2020<br></em>
        """.format(
            event_name=event.name, identifier=identifier
        )
        self._set_subject("Thanks for participating in {}".format(event.name))
        self._set_email(email)
        self._set_html_content(html_content)
        self._send()

    def send_payment_confirmation(self, team):
        html_content = """
        Hello,
        This to confirm you that we have received your payment for the \
        identifier <strong>{}</strong>.<br>
        Looking forward to see you at the event.<br><br>
        <em>Regards,<br>
        IT Team, ICT Fest 2020<br></em>
        """.format(
            team.team_identifier
        )
        self._set_subject(
            "Payment confirmation for {}".format(team.event.name)
        )
        self._set_email(team.team_members[0].email)
        self._set_html_content(html_content)
        self._send()

    def _send(self):
        try:
            sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
            response = sg.send(self.message)
            print(response.status_code)
            print(response.body)
        except Exception as e:
            print(e)
