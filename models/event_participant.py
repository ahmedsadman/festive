from application import db
from models.participant import ParticipantModel
from models.event import EventModel


class EventParticipantModel(db.Model):
    '''The association table (or secondary) between Event and Participant, to maintain 
    many to many relationship. Maps a participant to a particular event. This model will 
    be handled by SQLAlchemy, and should not be manipulated by others'''

    __tablename__ = 'event_participant'
    id = db.Column(db.Integer, primary_key=True)
    participant_id = db.Column(db.Integer, db.ForeignKey('participants.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    @classmethod
    def add_participant(cls, event_id, participant_id):
        '''adds a participant under an event'''
        event = EventModel.find_by_id(event_id)
        participant = ParticipantModel.find_by_id(participant_id)

        event.participants.append(participant)
        db.session.commit()

    @classmethod
    def list_participant(cls, event_id):
        '''return all the individual participants under an event'''
        event = EventModel.find_by_id(event_id)
        return event.participants
