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
    def get(self):
        '''find a participant by his email'''
        ps = ParticipantSchema(partial=True)
        data = ps.load(request.args)
        participant = ParticipantModel.find_by_email(data['email'])
        if participant:
            return ps.dump(participant)
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
        '''find a team by using filters from request arguments'''
        # partial -> allow skipping of required fields
        ts = TeamSchema(partial=True)
        try:
            _filter = ts.load(request.args)
        except ValidationError as err:
            return err.messages, 400

        # raise exception if zero argument is passed
        if not _filter.keys():
            raise BadRequest('No query arguments passed')

        team = TeamModel.find(_filter)
        return {
            'count': len(team),
            'data': TeamSchema(partial=True, many=True, exclude=('team_identifier',)).dump(team)
        }
