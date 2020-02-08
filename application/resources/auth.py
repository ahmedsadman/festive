from flask import request, Blueprint
from marshmallow import ValidationError
from flask_jwt_extended import create_access_token
from datetime import timedelta

from application.models import UserModel
from application.helpers.schemas import UserSchema
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
