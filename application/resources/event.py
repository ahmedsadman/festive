from flask import Blueprint, request
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required

from application.models import EventModel
from application.error_handlers import *
from application.schemas import EventRegistration, TeamSchema, EventSchema

event_bp = Blueprint("event", __name__)


@event_bp.route("/list", methods=["GET"])
def event_list():
    es = EventSchema()
    events = EventModel.find_all()
    return {"events": es.dump(events, many=True)}


@event_bp.route("/create", methods=["POST"])
@jwt_required
def create_event():
    """create a new event with the given name"""
    es = EventSchema()
    try:
        data = es.load(request.get_json())
    except ValidationError as err:
        return err.messages, 400

    event = EventModel(
        data["name"],
        data["payable_amount"],
        data["payable_school"],
        data["payable_college"],
        data["payable_university"],
        data["team_participation"],
        data["rulebook_url"],
    )
    event.save()
    return es.dump(event), 201


@event_bp.route("/<event_id>", methods=["GET"])
@jwt_required
def get_event(event_id):
    es = EventSchema()
    event = EventModel.find_by_id(event_id)
    if event:
        return es.dump(event)
    raise NotFound()


@event_bp.route("/<event_id>", methods=["DELETE"])
@jwt_required
def delete_event(event_id):
    event = EventModel.find_by_id(event_id)
    if event:
        event.delete()
        return {"message": "Event deleted successfully", "event": event.name}
    raise NotFound()


@event_bp.route("/<event_id>", methods=["PATCH"])
@jwt_required
def update_event(event_id):
    es = EventSchema(partial=True)
    data = es.load(request.get_json())
    event = EventModel.find_by_id(event_id)

    if event:
        for attr, value in data.items():
            setattr(event, attr, value)
        event.save()
        return {"message": "Event data updated", "data": es.dump(event)}
    raise NotFound()
