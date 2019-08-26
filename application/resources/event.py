from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from application.models.event import EventModel
from application.models.participant import ParticipantModel
from application.models.team import TeamModel
from application.error_handlers import *
from application.schemas import EventRegistration, TeamSchema, EventSchema


class EventCreate(Resource):
    def post(self):
        '''create a new event with the given name'''
        es = EventSchema()
        try:
            data = es.load(request.get_json())
            print(data)
        except ValidationError as err:
            return err.messages, 400

        event = EventModel(data['name'], data['payable_amount'])

        event.save()
        return es.dump(event), 201


class EventList(Resource):
    '''Handles list of events with specific information like number of participants'''
    # number of participants not implemented yet

    def get(self):
        es = EventSchema()
        events = EventModel.find_all()
        return {'events': es.dump(events, many=True)}
