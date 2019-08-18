from flask_restful import Resource, reqparse
from application.models.team import TeamModel
from application.error_handlers import *


class Team(Resource):
    def post(self, name, event_id):
        if TeamModel.find(name, event_id):
            raise BadRequest(message='A team with the given name already exists')
        team = TeamModel(name, event_id)
        team.save()
        return team.json(), 201

    def get(self, name, event_id):
        team = TeamModel.find(name, event_id)
        if team:
            return team.json()
        raise NotFound(message='Team not found')