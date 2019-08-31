from application import db
from application.models.basemodel import BaseModel


class PaymentModel(BaseModel):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    # unique required for one to one relationship
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), unique=True)
    transaction_no = db.Column(db.String(50), nullable=True)
    status = db.Column(db.Boolean, default=False)

    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    # team -> backref from payment model

    def __init__(self, team_id):
        self.team_id = team_id
