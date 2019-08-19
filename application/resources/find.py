from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from application.error_handlers import *
from application.models.participant import ParticipantModel
from application.models.event import EventModel
from application.models.team import TeamModel
from application.schemas import ParticipantSchema
from application.schemas import TeamSchema

# find details about different entity


class FindParticipant(Resource):
    def get(self, email):
        '''find a participant by his email'''
        participant = ParticipantModel.find_by_email(email)
        if participant:
            ps = ParticipantSchema()
            return ps.dump(participant)
            # return participant.json()
        raise NotFound()


class FindEvent(Resource):
    def get(self, name):
        '''find an event by name'''
        event = EventModel.find_by_name(name)
        if event:
            return event.json()
        raise NotFound()


class FindTeam(Resource):
    def get(self):
        '''find a team by using filers from request arguments'''
        # partial -> allow skipping of required fields
        ts = TeamSchema(partial=('name', 'event_id'))
        try:
            _filter = ts.load(request.args)
        except ValidationError as err:
            return err.messages, 400

        # raise exception if zero argument is passed
        if not _filter.keys(): raise NotFound()
            
        team = TeamModel.find(**_filter)
        if team:
            return ts.dump(team)
        raise NotFound()
