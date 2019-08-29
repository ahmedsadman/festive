from datetime import datetime
from application import db
from application.models.basemodel import BaseModel


class ParticipantModel(BaseModel):
    __tablename__ = 'participants'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    email = db.Column(db.String(30), unique=True)
    institute = db.Column(db.String(60), nullable=True)
    contact_no = db.Column(db.String(30), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)

    # for many to many relationship, maps user to events/teams
    events = db.relationship('EventModel', secondary='event_participant', lazy='dynamic',
                             backref=db.backref('participants', lazy='dynamic'))
    teams = db.relationship('TeamModel', secondary='team_participant', lazy='dynamic',
                            backref=db.backref('team_members', lazy='dynamic'))

    def __init__(self, name, email, institute=None):
        self.name = name
        self.email = email
        self.institute = institute

    def has_participated_event(self, event_id):
        return self.events.filter_by(id=event_id).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
