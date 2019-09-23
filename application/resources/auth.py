from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from flask_jwt_extended import create_access_token
from datetime import timedelta

from application.models.user import UserModel
from application.schemas import UserSchema
from application.error_handlers import *


class Register(Resource):
    """Register an user with username and password"""

    def post(self):
        us = UserSchema()
        try:
            data = us.load(request.get_json())
        except ValidationError as err:
            raise FieldValidationFailed(error=err.messages)

        # check if the user already exists
        if UserModel.find_by_username(data["username"]):
            raise BadRequest(
                message='The username "{}" already exists'.format(
                    data["username"]
                )
            )

        user = UserModel(data["username"], data["password"])
        user.save()
        return UserSchema(exclude=("password",)).dump(user)


class Login(Resource):
    def post(self):
        us = UserSchema()
        try:
            data = us.load(request.get_json())
        except ValidationError as err:
            raise FieldValidationFailed(error=err.messages)

        # find the user
        user = UserModel.find_by_username(data["username"])

        # match password and then send access token if valid
        if user and user.check_password(data["password"]):
            expires = timedelta(days=1)  # token will expire after 1 day
            access_token = create_access_token(
                identity=user.id, fresh=True, expires_delta=expires
            )
            return {"access_token": access_token}
        raise AuthorizationError(
            message="Invalid credentials",
            error=AuthorizationError.INVALID_CRED,
        )
