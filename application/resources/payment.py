from flask import request
from marshmallow import ValidationError
from flask_restful import Resource
from application.models.payment import PaymentModel


class Payment(Resource):
    def get(self):
        return None
