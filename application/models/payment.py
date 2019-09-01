from datetime import datetime
from application import db
from application.models.basemodel import BaseModel


class PaymentModel(BaseModel):
    __tablename__ = 'payments'
    PAYMENT_PENDING = 'pending'
    PAYMENT_WAITING = 'waiting'
    PAYMENT_OK = 'ok'
    
    id = db.Column(db.Integer, primary_key=True)
    # unique required for one to one relationship
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), unique=True)
    transaction_no = db.Column(db.String(50), nullable=True)
    status = db.Column(db.String(20), default='pending')

    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    updated_on = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # team -> backref from payment model

    def __init__(self, team_id):
        self.team_id = team_id
