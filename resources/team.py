from flask_restful import Resource, reqparse
from models.team import TeamModel


class Team(Resource):
    def post(self, name, event_id):
        if TeamModel.find_by_name(name):
            return {'message': 'A team with the name "{}" already exists'.format(name)}
        team = TeamModel(name, event_id)
        team.save()
        return team.json(), 201

    def get(self, name):
        team = TeamModel.find_by_name(name)
        if team:
            return team.json()
        return {'message': 'Team not found'}, 400