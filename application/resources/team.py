from flask import request, Blueprint
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required

from application.helpers.auth_helper import super_admin_required
from application.helpers.schemas import TeamSchema, PaginatedResponse
from application.models.team import TeamModel
from application.helpers.error_handlers import *

team_bp = Blueprint("team", __name__)


@team_bp.route("/<team_id>", methods=["GET"])
@jwt_required
def get_team(team_id):
    ts = TeamSchema(partial=True)
    team = TeamModel.find_by_id(team_id)
    if team:
        return ts.dump(team)
    raise NotFound()


@team_bp.route("/<team_id>", methods=["DELETE"])
@super_admin_required
def delete_team(team_id):
    team = TeamModel.find_by_id(team_id)
    if team:
        team.delete()
        return {"message": "Successfully deleted"}
    raise NotFound()


@team_bp.route("/find", methods=["GET"])
def find_team():
    """find a team by using filters from request arguments"""
    # partial -> allow skipping of required fields
    ts = TeamSchema(
        partial=True,
        only=(
            "name",
            "event_id",
            "team_identifier",
            "payment_status",
            "single",
            "page",
        ),
    )
    try:
        _filter = ts.load(request.args)
    except ValidationError as err:
        raise FieldValidationFailed(error=err.messages)

    team_paginated = TeamModel.find(_filter)  # returns pagination obj
    pagination_response = PaginatedResponse(
        team_paginated,
        TeamSchema(
            partial=True,
            many=True,
            exclude=("team_identifier", "event_id", "payment.transaction_no"),
        ),
    )
    return pagination_response.dump()
