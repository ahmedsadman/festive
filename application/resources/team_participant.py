from flask_restful import Resource, reqparse
from application.models.team_participant import TeamParticipantModel


class TeamParticipant(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('team_id', type=int, required=True)
    parser.add_argument('participant_id', type=int, required=False)

    def get(self):
        '''Return all team members under a team'''
        data = TeamParticipant.parser.parse_args()
        team_members = TeamParticipantModel.list_members(data['team_id'])
        return {'members': [m.json() for m in team_members.all()]}
