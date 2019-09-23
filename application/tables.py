from application import db

"""Declare raw tables that does not require to inherit db.Model"""

# team and participant association table for many to many relation
team_participant = db.Table(
    "team_participant",
    db.Column("id", db.Integer, primary_key=True),
    db.Column("participant_id", db.Integer, db.ForeignKey("participants.id")),
    db.Column("team_id", db.Integer, db.ForeignKey("teams.id")),
)

# event and participant association table for many to many relation
event_participant = db.Table(
    "event_participant",
    db.Column("id", db.Integer, primary_key=True),
    db.Column("participant_id", db.Integer, db.ForeignKey("participants.id")),
    db.Column("event_id", db.Integer, db.ForeignKey("events.id")),
)
