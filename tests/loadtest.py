"""Tests server load by applying read/write operations"""

from locust import HttpLocust, TaskSet, task
import random
import string


class UserBehavior(TaskSet):
    EVENT_IDS = [1, 2, 3]
    PAYMENT_STATUS = ["pending", "waiting", "ok"]

    def _random_string(self, n):
        return "".join(random.choices(string.ascii_uppercase, k=n))

    def generate_data(self):
        return {
            "participants": [
                {
                    "name": self._random_string(10),
                    "email": "{}@gmail.com".format(self._random_string(6)),
                    "tshirt_size": "l",
                    "institute": "IUT",
                    "contact_no": "01715002073",
                },
                {
                    "name": self._random_string(10),
                    "email": "{}@gmail.com".format(self._random_string(6)),
                    "tshirt_size": "l",
                    "institute": "IUT",
                    "contact_no": "01715002073",
                },
            ],
            "team_name": self._random_string(5),
        }

    @task
    def index(self):
        response = self.client.get("/")

    @task
    def list_events(self):
        response = self.client.get("/events")

    @task
    def find_team_by_event(self):
        event_id = random.choice(self.EVENT_IDS)
        response = self.client.get("/team/find?event_id={}".format(event_id))

    @task
    def find_team_by_payment(self):
        status = random.choice(self.PAYMENT_STATUS)
        response = self.client.get(
            "/team/find?payment_status={}".format(status)
        )

    @task
    def find_participant_by_event(self):
        event_id = random.choice(self.EVENT_IDS)
        response = self.client.get(
            "/participant/find?event_id={}".format(event_id)
        )

    @task
    def event_register(self):
        response = self.client.post(
            "/event/register/1", json=self.generate_data()
        )
        print(response)


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 3000
    max_wait = 7000
