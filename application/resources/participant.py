from flask import request
from marshmallow import ValidationError
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from application.models.participant import ParticipantModel
from application.error_handlers import BadRequest, NotFound
from application.schemas import ParticipantSchema, PaginatedResponse


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
            return {"message": "Successfully deleted"}
        raise NotFound()


class FindParticipant(Resource):
    def get(self):
        """find participants by query filters"""
        ps = ParticipantSchema(
            partial=True, only=("name", "email", "event_id", "page")
        )

        try:
            _filter = ps.load(request.args)
        except ValidationError as err:
            return err.messages

        participant_paginated = ParticipantModel.find(_filter)
        pagination_response = PaginatedResponse(
            participant_paginated,
            ParticipantSchema(many=True, exclude=("contact_no",)),
        )
        return pagination_response.dump()
