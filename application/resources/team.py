from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required

from application.schemas import TeamSchema
from application.models.team import TeamModel
from application.error_handlers import *


class Team(Resource):
    @jwt_required
    def get(self, team_id):
        ts = TeamSchema(partial=True)
        team = TeamModel.find_by_id(team_id)
        if team:
            return ts.dump(team)
        raise NotFound()

    @jwt_required
    def delete(self, team_id):
        team = TeamModel.find_by_id(team_id)
        if team:
            team.delete()
            return {'message': 'Successfully deleted'}
        raise NotFound()


class FindTeam(Resource):
    def get(self):
        '''find a team by using filters from request arguments'''
        # partial -> allow skipping of required fields
        ts = TeamSchema(partial=True, only=(
            'name', 'event_id', 'team_identifier'))
        try:
            _filter = ts.load(request.args)
        except ValidationError as err:
            raise FieldValidationFailed(error=err.messages)

        # raise exception if zero argument is passed
        if not _filter.keys():
            raise BadRequest('No query arguments passed')

        team = TeamModel.find(_filter)
        return {
            'count': len(team),
            'data': TeamSchema(partial=True, many=True, exclude=('team_identifier', 'payment.transaction_no')).dump(team)
        }
