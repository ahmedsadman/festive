from flask import request
from marshmallow import ValidationError
from flask_restful import Resource
from application.models.participant import ParticipantModel
from application.error_handlers import BadRequest
from application.schemas import ParticipantSchema


class Participant(Resource):
    def post(self):
        ps = ParticipantSchema()

        try:
            data = ps.load(request.get_json())
        except ValidationError as err:
            return err.messages, 400

        if ParticipantModel.find_by_email(data['email']):
            raise BadRequest(message='The email is already registered')

        participant = ParticipantModel(
            data['name'], data['email'], data['is_leader'], data['institute'])
        participant.save()
        ps = ParticipantSchema(only=('id', 'name'))
        return ps.dump(participant), 201
