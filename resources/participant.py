from flask_restful import Resource, reqparse
from models.participant import ParticipantModel


class Participant(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True)
    parser.add_argument('email', type=str, required=True)
    parser.add_argument('institute', type=str, required=False)
    parser.add_argument('is_leader', type=bool, required=False)

    def post(self):
        data = Participant.parser.parse_args()

        if ParticipantModel.find(data['email']):
            return {'message': 'A participant with the email "{}" already exists'.format(data['email'])}, 400

        participant = ParticipantModel(data['name'], data['email'], data['is_leader'], data['institute'])
        participant.save()
        return participant.json(), 201
        
