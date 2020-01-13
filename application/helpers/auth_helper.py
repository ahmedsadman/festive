from functools import wraps
from flask_jwt_extended import get_jwt_claims, verify_jwt_in_request
from application import jwt
from application.models import UserModel


@jwt.user_claims_loader
def add_claims(id):
    user = UserModel.find_by_id(id)
    return {"super_admin": user.is_super_admin()}


def super_admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()

        if claims["super_admin"] is False:
            return ({"message": "The operation requires super admin"}, 403)
        return fn(*args, **kwargs)

    return wrapper
