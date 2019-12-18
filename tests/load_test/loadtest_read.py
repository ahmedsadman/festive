"""Tests server load by applying various read operations only"""

from locust import HttpLocust, TaskSet, task
from random import choice


class UserBehavior(TaskSet):
    EVENT_IDS = [1, 2, 3]
    PAYMENT_STATUS = ["pending", "waiting", "ok"]

    @task(1)
    def index(self):
        response = self.client.get("/")

    @task(1)
    def list_events(self):
        response = self.client.get("/events")

    @task(2)
    def find_team_by_event(self):
        event_id = choice(self.EVENT_IDS)
        response = self.client.get("/team/find?event_id={}".format(event_id))

    @task(2)
    def find_team_by_payment(self):
        status = choice(self.PAYMENT_STATUS)
        response = self.client.get(
            "/team/find?payment_status={}".format(status)
        )

    @task(2)
    def find_participant_by_event(self):
        event_id = choice(self.EVENT_IDS)
        response = self.client.get(
            "/participant/find?event_id={}".format(event_id)
        )


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 2000
    max_wait = 5000
