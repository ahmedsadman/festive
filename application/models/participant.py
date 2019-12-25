from datetime import datetime
from sqlalchemy import desc
from application import db
from application.models import BaseModel


class ParticipantModel(BaseModel):
    __tablename__ = "participants"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    email = db.Column(db.String(60), unique=True, index=True)
    institute = db.Column(db.String(60), nullable=True)
    tshirt_size = db.Column(db.String(10))
    contact_no = db.Column(db.String(30), nullable=True)

    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    updated_on = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # for many to many relationship, maps user to events/teams
    events = db.relationship(
        "EventModel",
        secondary="event_participant",
        lazy="dynamic",
        backref=db.backref("participants", lazy="dynamic"),
    )
    teams = db.relationship(
        "TeamModel",
        secondary="team_participant",
        lazy="dynamic",
        backref=db.backref("team_members", lazy="dynamic"),
    )

    def __init__(self, name, email, tshirt_size, institute, contact_no=None):
        self.name = name
        self.email = email
        self.tshirt_size = tshirt_size
        self.institute = institute
        self.contact_no = contact_no

    def has_participated_event(self, event_id):
        return self.events.filter_by(id=event_id).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find(cls, _filter):
        """find participant(s) based on given filters (in request arg),
        returns pagination obj"""

        # remove any relationship based filters first
        event_id = _filter.pop("event_id", None)

        # seperate non-filter arguments (like pagination)
        page = _filter.pop("page", 1)

        # build the simple query
        query = super().find_query(_filter)

        # now process any relationship filter if available
        if event_id is not None:
            query = query.join(cls.events).filter_by(id=event_id)

        # finally return pagination object, sorted descending
        return query.order_by(desc(cls.created_on)).paginate(
            page=page, per_page=10, error_out=True
        )
