from flask_restful import Resource, reqparse
from models.participant import ParticipantModel
from application.error_handlers import BadRequest

class Participant(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True)
    parser.add_argument('email', type=str, required=True)
    parser.add_argument('institute', type=str, required=False)
    parser.add_argument('is_leader', type=bool, required=False)

    def post(self):
        data = Participant.parser.parse_args()

        if ParticipantModel.find(data['email']):
            raise BadRequest(message='The email is already registered')

        participant = ParticipantModel(data['name'], data['email'], data['is_leader'], data['institute'])
        participant.save()
        return participant.json(), 201
        
