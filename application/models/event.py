from application import db
from application.models import BaseModel


class EventModel(BaseModel):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    active = db.Column(db.Boolean, default=True)
    payable_amount = db.Column(db.Integer)
    payable_school = db.Column(db.Integer, nullable=True)
    payable_college = db.Column(db.Integer, nullable=True)
    payable_university = db.Column(db.Integer, nullable=True)
    rulebook_url = db.Column(db.String(80), nullable=True)

    # whether the event is meant to be participated under a team
    team_participation = db.Column(db.Boolean)

    teams = db.relationship("TeamModel", backref="event", lazy="dynamic")
    # participants -> backref from participant model

    def __init__(
        self,
        name,
        payable_amount,
        payable_school=None,
        payable_college=None,
        payable_university=None,
        team_participation=False,
        rulebook_url=None,
    ):
        self.name = name
        self.payable_amount = payable_amount
        self.payable_school = payable_school
        self.payable_college = payable_college
        self.payable_university = payable_university
        self.team_participation = team_participation
        self.rulebook_url = rulebook_url

    def add_participant(self, participant):
        """adds a participant under the event"""
        self.participants.append(participant)
        db.session.commit()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
