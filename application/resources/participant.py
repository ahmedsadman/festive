from flask import request
from marshmallow import ValidationError
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from application.models.participant import ParticipantModel
from application.error_handlers import BadRequest, NotFound
from application.schemas import ParticipantSchema


class Participant(Resource):
    @jwt_required
    def get(self, participant_id):
        ps = ParticipantSchema()
        participant = ParticipantModel.find_by_id(participant_id)

        if participant:
            return ps.dump(participant)
        raise NotFound

    @jwt_required
    def delete(self, participant_id):
        ps = ParticipantSchema(partial=True)
        participant = ParticipantModel.find_by_id(participant_id)
        
        if participant:
            participant.delete()
            return {'message': 'Successfully deleted'}
        raise NotFound()
        

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
            'count': len(participant),
            'data': ParticipantSchema(many=True, exclude=('contact_no',)).dump(participant)
        }
