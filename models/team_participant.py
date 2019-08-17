from application import db
from models.participant import ParticipantModel
from models.team import TeamModel


class TeamParticipantModel(db.Model):
    '''The association table (or secondary) between Team and Participant, to maintain 
    many to many relationship. Maps a participant to a team. This model will 
    be handled by SQLAlchemy, and should not be manipulated by others'''

    __tablename__ = 'team_participant'
    id = db.Column(db.Integer, primary_key=True)
    participant_id = db.Column(db.Integer, db.ForeignKey('participants.id'))
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))

    @classmethod
    def add_member(cls, participant_id, team_id):
        '''add a participant in a team'''
        team = TeamModel.find_by_id(team_id)
        participant = ParticipantModel.find_by_id(participant_id)

        team.team_members.append(participant)
        db.session.commit()

    @classmethod
    def list_members(cls, team_id):
        '''list all the team members under a given team'''
        team = TeamModel.find_by_id(team_id)
        return team.team_members