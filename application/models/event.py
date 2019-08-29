from application import db
from application.models.basemodel import BaseModel


class EventModel(BaseModel):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    payable_amount = db.Column(db.Integer)

    teams = db.relationship('TeamModel', backref='event', lazy='dynamic')
    # participants -> backref from participant model

    def __init__(self, name, payable_amount):
        self.name = name
        self.payable_amount = payable_amount

    def add_participant(self, participant):
        '''adds a participant under the event'''
        self.participants.append(participant)
        db.session.commit()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
