from flask import request, Blueprint
from marshmallow import ValidationError
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
)
from datetime import timedelta

from application.models import UserModel
from application.helpers.schemas import UserSchema, PasswordResetSchema
from application.helpers.error_handlers import *

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    us = UserSchema(only=("username", "password"))
    try:
        data = us.load(request.get_json())
    except ValidationError as err:
        raise FieldValidationFailed(error=err.messages)

    # find the user
    user = UserModel.find_by_username(data["username"])

    # match password and then send access token if valid
    if user and user.check_password(data["password"]):
        expires = timedelta(minutes=15)  # token will expire after 15 min
        access_token = create_access_token(
            identity=user.id, fresh=True, expires_delta=expires
        )
        return {"access_token": access_token}
    raise AuthorizationError(
        message="Invalid credentials", error=AuthorizationError.INVALID_CRED
    )


@auth_bp.route("/reset/password", methods=["POST"])
@jwt_required
def reset_password():
    pr = PasswordResetSchema()
    try:
        data = pr.load(request.get_json())
    except ValidationError as err:
        raise FieldValidationFailed(error=err.messages)

    user_id = get_jwt_identity()
    user = UserModel.find_by_id(user_id)

    if user.reset_password(data["old_pass"], data["new_pass"]):
        return {"message": "Success"}
    return {"message": "Error due to wrong credentials"}, 400
