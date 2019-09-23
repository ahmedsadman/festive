from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required

from application.models.event import EventModel
from application.models.participant import ParticipantModel
from application.models.team import TeamModel
from application.error_handlers import *
from application.schemas import EventRegistration, TeamSchema, EventSchema


class Event(Resource):
    @jwt_required
    def get(self, event_id):
        es = EventSchema()
        event = EventModel.find_by_id(event_id)
        if event:
            return es.dump(event)
        raise NotFound()

    @jwt_required
    def patch(self, event_id):
        es = EventSchema(partial=True)
        data = es.load(request.get_json())
        event = EventModel.find_by_id(event_id)

        if event:
            for attr, value in data.items():
                setattr(event, attr, value)
            event.save()
            return {"message": "Event data updated"}
        raise NotFound()

    @jwt_required
    def delete(self, event_id):
        event = EventModel.find_by_id(event_id)
        if event:
            event.delete()
            return {"message": "Event deleted successfully"}
        raise NotFound()


class EventCreate(Resource):
    @jwt_required
    def post(self):
        """create a new event with the given name"""
        es = EventSchema()
        try:
            data = es.load(request.get_json())
        except ValidationError as err:
            raise FieldValidationFailed(error=err.messages)

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


class EventList(Resource):
    """Handles list of events with specific information like number
    of participants"""

    # number of participants not implemented yet

    def get(self):
        es = EventSchema()
        events = EventModel.find_all()
        return {"events": es.dump(events, many=True)}
