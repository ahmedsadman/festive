from flask import request
from marshmallow import ValidationError
from flask_restful import Resource
from application.models.participant import ParticipantModel
from application.error_handlers import BadRequest, NotFound
from application.schemas import ParticipantSchema


class FindParticipant(Resource):
    def get(self):
        '''find participants by query filters'''
        ps = ParticipantSchema(partial=True, only=('name', 'email'))

        try:
            _filter = ps.load(request.args)
        except ValidationError as err:
            return err.messages

        if not _filter.keys():
            raise BadRequest(message='No query arguments passed')

        participant = ParticipantModel.find(_filter)
        return {
            'found': len(participant) > 0,
            'count': len(participant),
            'data': ParticipantSchema(many=True).dump(participant)
        }
