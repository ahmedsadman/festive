import pytest
import json
from application import create_app
from dotenv import load_dotenv
from config import Config


def test_homepage(client):
    r = client.get("/")
    assert r.status_code == 200


def test_events(client):
    r = client.get("/events")
    # res = json.loads(r.data)
    assert r.status_code == 200
