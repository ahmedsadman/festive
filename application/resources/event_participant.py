from flask_restful import Resource, reqparse
from application.models.event_participant import EventParticipantModel
from application.schemas import ParticipantSchema

class EventParticipant(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('event_id', type=int, required=True)
    parser.add_argument('participant_id', type=int, required=False)

    def post(self):
        '''Add participant to an event'''
        data = EventParticipant.parser.parse_args()
        EventParticipantModel.add_participant(data['event_id'], data['participant_id'])
        return {'message': 'Successfully added'}
