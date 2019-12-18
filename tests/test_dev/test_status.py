import pytest
import json
from application import create_app
from dotenv import load_dotenv
from config import Config

"""Test the status code for all routes"""


def test_homepage(client):
    r = client.get("/")
    assert r.status_code == 200


def test_events(client):
    r = client.get("/events")
    # res = json.loads(r.data)
    assert r.status_code == 200


def test_event_get(client):
    r = client.get("/event/1")
    assert r.status_code == 401


def test_participant_get(client):
    r = client.get("/participant/1")
    assert r.status_code == 401


def test_participant_find(client):
    r = client.get("/participant/find?event_id=1")
    assert r.status_code == 200

    r = client.get("/participant/find?email=test@gmail.com")
    assert r.status_code == 200

    r = client.get("/participant/find?email=test@gmail.com")
    assert r.status_code == 200


def test_team_get(client):
    r = client.get("/team/1")
    assert r.status_code == 401


def test_team_find(client):
    r = client.get("/team/find?event_id=1")
    assert r.status_code == 200

    r = client.get("/team/find?name=abcd")
    assert r.status_code == 200

    r = client.get("/team/find?team_identifier=HACK1234")
    assert r.status_code == 200

    r = client.get("/team/find?payment_status=pending")
    assert r.status_code == 200

    r = client.get("/team/find?single=true")
    assert r.status_code == 200
