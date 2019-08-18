from flask_restful import Resource
from application.error_handlers import *
from application.models.participant import ParticipantModel
from application.models.event import EventModel
from application.models.team import TeamModel

# find details about different entity


class FindParticipant(Resource):
    def get(self, email):
        '''find a participant by his email'''
        participant = ParticipantModel.find_by_email(email)
        if participant:
            return participant.json()
        raise NotFound()


class FindEvent(Resource):
    def get(self, name):
        '''find an event by name'''
        event = EventModel.find_by_name(name)
        if event:
            return event.json()
        raise NotFound()


class FindTeam(Resource):
    def get(self, name, event_id):
        '''find a team by it's name'''
        team = TeamModel.find(name, event_id)
        if team:
            return team.json()
        raise NotFound()
