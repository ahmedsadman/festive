from application import db
from application.models.basemodel import BaseModel


class PaymentModel(BaseModel):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    transaction_no = db.Column(db.String(50), nullable=True)
    status = db.Column(db.Boolean, default=False)

    def __init__(self, team_id):
        self.team_id = team_id