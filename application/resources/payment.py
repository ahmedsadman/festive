from flask import request, Blueprint
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required

from application.models.payment import PaymentModel
from application.schemas import PaymentSchema
from application.models.team import TeamModel
from application.mailer import Mailer
from application.error_handlers import *

payment_bp = Blueprint("payment", __name__)


@payment_bp.route("/<team_identifier>", methods=["POST"])
def request_payment_verify(team_identifier):
    """Requests for payment verification. Participant provides transcation no
    of payment."""
    ps = PaymentSchema(partial=True, only=("transaction_no",))
    try:
        data = ps.load(request.get_json())
    except ValidationError as err:
        raise FieldValidationFailed(error=err.messages)

    team = TeamModel.find_by_identifier(team_identifier)
    if not team:
        raise NotFound(message="Team not found")

    payment = team.payment

    if payment.transaction_no:
        raise BadRequest(
            message="The team has already requested for payment \
                verification"
        )

    payment.transaction_no = data["transaction_no"]
    payment.status = PaymentModel.PAYMENT_WAITING
    payment.save()
    return {"message": "Success"}


@payment_bp.route("/verify/<team_id>", methods=["POST"])
@jwt_required
def verify_payment(team_id):
    """Verify payment of participants from admin side"""
    team = TeamModel.find_by_id(team_id)
    if not team:
        raise NotFound(message="The team was not found")

    payment = team.payment

    if payment.status == PaymentModel.PAYMENT_OK:
        raise BadRequest(message="Payment is already verified")

    if payment.transaction_no:
        payment.status = PaymentModel.PAYMENT_OK
        payment.save()

        # send confirmation email
        mailer = Mailer()
        mailer.send_payment_confirmation(team)

        return {"message": "Payment verified"}

    raise BadRequest(message="No transaction found for the given team")
