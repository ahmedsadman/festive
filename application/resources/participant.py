from flask import request, Blueprint
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required

from application.helpers.auth_helper import super_admin_required
from application.models import ParticipantModel
from application.error_handlers import BadRequest, NotFound
from application.schemas import ParticipantSchema, PaginatedResponse

participant_bp = Blueprint("participant", __name__)


@participant_bp.route("/<participant_id>", methods=["GET"])
@jwt_required
def get_participant(participant_id):
    ps = ParticipantSchema()
    participant = ParticipantModel.find_by_id(participant_id)

    if participant:
        return ps.dump(participant)
    raise NotFound


@participant_bp.route("/<participant_id>", methods=["DELETE"])
@super_admin_required
def delete_participant(participant_id):
    ps = ParticipantSchema(partial=True)
    participant = ParticipantModel.find_by_id(participant_id)

    if participant:
        participant.delete()
        return {"message": "Successfully deleted"}
    raise NotFound()


@participant_bp.route("/find", methods=["GET"])
def find_participant():
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
