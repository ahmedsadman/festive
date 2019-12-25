import string
import random
from datetime import datetime
from sqlalchemy import func, desc

from application import db
from application.models import BaseModel


class TeamModel(BaseModel):
    """Model for Teams. In any fest, there are some events where people
    participate as teams,
    for example 'Hackthon' or 'Programming Contest'. Again there are some
    events, where single
    participation is expected, such as 'Math Olympiads'. Whether single
    participant or multiple participants, all of them are considered
    as a team . If single participant is expected, the value of the
    field 'single' will be set to True, based
    on the event parameters and the team name will be participant's name."""

    __tablename__ = "teams"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    # indicates whether a team should consist of only one member
    single = db.Column(db.Boolean, default=False)

    event_id = db.Column(db.Integer, db.ForeignKey("events.id"))
    team_identifier = db.Column(
        db.String(50), nullable=True, unique=True, index=True
    )
    participation_level = db.Column(db.String(20))

    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    updated_on = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    payment = db.relationship("PaymentModel", backref="team", uselist=False)

    # team_members -> backref from participant model
    # event -> backref from event model

    def __init__(self, name, single, event_id, participation_level=None):
        self.name = name
        self.single = single
        self.event_id = event_id
        self.participation_level = participation_level

    def save(self):
        db.session.add(self)
        db.session.flush()
        self.team_identifier = self._generate_identifier()
        db.session.commit()

    def _random_string(self, n):
        return "".join(random.choices(string.ascii_uppercase, k=n))

    def _generate_identifier(self):
        # first 4 char of event name (upper) + last 3 char of timestamp
        # + random string of len 2 + id
        if not self.id:
            raise ValueError("ID is not defined")
        stamp = str(int(self.created_on.timestamp()))[-3:]
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
        """find team(s) based on filter data. returns pagination object"""

        # -- first remove any relationship based filters so that normal
        # filtering can be done at first --
        # payment_status requires realtionship attribute and requires
        # different query.
        # So remove it from filters and store it in other place to process
        # later
        payment_status = _filter.pop("payment_status", None)

        # seperate non-filter arguments (like pagination arguments)
        page = _filter.pop("page", 1)

        # now the filters has only level one query attribute, build
        # the simple query
        query = super().find_query(_filter)

        # now process any relationship filter if available
        if payment_status is not None:
            query = query.join(cls.payment).filter_by(status=payment_status)

        # finally return pagination object, sorted descending
        return query.order_by(desc(cls.created_on)).paginate(
            page=page, per_page=10, error_out=True
        )
