import string
import random
from datetime import datetime
from sqlalchemy import func

from application import db
from application.models.basemodel import BaseModel


class TeamModel(BaseModel):
    '''Model for Teams. In any fest, there are some events where people participate as teams,
    for example 'Hackthon' or 'Programming Contest'. Again there are some events, where single 
    participation is expected, such as 'Math Olympiads'. Whether single participant 
    or multiple participants, all of them are considered as a team. Only difference is, if single
    participant is expected, just set the 'single' value to true, which says that the team is a
    pseudo-team and should contain only one member. For this case, team name should be the
    participant's name'''

    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    # indicates whether a team should consist of only one member
    single = db.Column(db.Boolean, default=False)

    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    team_identifier = db.Column(
        db.String(50), nullable=True, unique=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    payment = db.relationship('PaymentModel', backref='team', uselist=False)

    # team_members -> backref from participant model
    # event -> backref from event model

    def __init__(self, name, single, event_id):
        self.name = name
        self.single = single
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

    @classmethod
    def find_by_identifier(cls, identifier):
        return cls.query.filter_by(team_identifier=identifier).first()

    @classmethod
    def find(cls, _filter):
        # -- first remove any relationship based filters so that normal filtering can be done at first --
        # payment_status requires realtionship attribute and requires different query.
        # So remove it from filters and store it in other place to process later
        payment_status = _filter.pop('payment_status', None)

        # now the filters has only level one query attribute, build the simple query
        query = super().find_query(_filter)

        # now process any relationship filter if available
        if payment_status is not None:
            query = query.join(cls.payment).filter_by(status=payment_status)

        return query.all()
