"""Tests server load by applying various write operations only"""

from locust import HttpLocust, TaskSet, task
import string
import random


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
    def event_register(self):
        response = self.client.post(
            "/register/1", json=self.generate_data()
        )
        print(response)


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 2000
    max_wait = 5000
