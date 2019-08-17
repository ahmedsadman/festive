from application import db
from models.participant import ParticipantModel
from models.team import TeamModel


class TeamParticipantModel(db.Model):
    __tablename__ = 'team_participant'
    id = db.Column(db.Integer, primary_key=True)
    participant_id = db.Column(db.Integer, db.ForeignKey('participants.id'))
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))

    @classmethod
    def add_member(cls, participant_id, team_id):
        team = TeamModel.find_by_id(team_id)
        participant = ParticipantModel.find_by_id(participant_id)

        team.team_members.append(participant)
        db.session.commit()

    @classmethod
    def list_members(cls, team_id):
        team = TeamModel.find_by_id(team_id)
        return team.team_members