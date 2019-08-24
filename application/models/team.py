from application import db
from sqlalchemy import func
from datetime import datetime


class TeamModel(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    team_identifier = db.Column(db.String(50), nullable=True) # will handle later
    payment_status = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

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

    def _generate_identifier(self):
        # first 4 char of event name (upper) + last 4 char of timestamp + id
        if not self.id:
            raise ValueError('ID is not defined')
        stamp = str(int(self.created_at.timestamp()))[-4:]
        event_short = self.event.name.upper()[:4]
        return event_short + stamp + repr(self.id)

    def add_participant(self, participant):
        self.team_members.append(participant)
        db.session.commit()

    @classmethod
    def find(cls, _filter):
        '''find a team by given filter'''
        query = cls.query
        for attr, value in _filter.items():
            query = query.filter(func.lower(getattr(cls, attr)) == func.lower(value))
        return query.all()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()