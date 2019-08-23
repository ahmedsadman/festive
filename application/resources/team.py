from flask import request
from flask_restful import Resource
from application.models.team import TeamModel
from application.error_handlers import *
from application.schemas import TeamSchema


class Team(Resource):
    def post(self):
        '''Create a new team'''
        ts = TeamSchema(only=('name', 'event_id'))
        data = ts.load(request.get_json())

        if TeamModel.find(**data):
            raise BadRequest(message='A team with the given name already exists')
        team = TeamModel(data['name'], data['event_id'])
        team.save()
        return team.json(), 201