import string
import random
from datetime import datetime
from sqlalchemy import func

from application import db
from application.models.basemodel import BaseModel


class TeamModel(BaseModel):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    team_identifier = db.Column(db.String(50), nullable=True, unique=True, index=True)
    # here we can't use db.func() or server_default for time generation, because in team
    # identity generation we are using obj.timestamp(), which can only be done via python
    # datetime module
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    payment = db.relationship('PaymentModel', backref='team', uselist=False)

    # team_members -> backref from participant model
    # event -> backref from event model
    
    def __init__(self, name, event_id):
        self.name = name
        self.event_id = event_id

    def save(self):
        db.session.add(self)
        db.session.flush()
        self.team_identifier = self._generate_identifier()
        db.session.commit()

    def _random_string(self, n):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=n))

    def _generate_identifier(self):
        # first 4 char of event name (upper) + last 3 char of timestamp + random string of len 2 + id
        if not self.id:
            raise ValueError('ID is not defined')
        stamp = str(int(self.created_at.timestamp()))[-3:]
        event_short = self.event.name.upper()[:4].strip()
        random_str = self._random_string(2)
        return event_short + stamp + random_str + repr(self.id)

    def add_participant(self, participant):
        self.team_members.append(participant)
        db.session.commit()