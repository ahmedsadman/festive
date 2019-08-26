from flask import request
from flask_restful import Resource
from application.models.event import EventModel
from application.models.participant import ParticipantModel
from application.models.team import TeamModel
from application.error_handlers import *
from application.schemas import EventRegistration, TeamSchema, EventSchema


class EventRegister(Resource):
    '''Handle event registrations for teams/participants'''

    def post(self, event_id):
        '''register participants under an event
        handles user creation, team creation and mapping in one place'''

        # parse data
        er_schema = EventRegistration()
        try:
            data = er_schema.load(request.get_json())
        except ValidationError as err:
            return err.messages, 400

        event = EventModel.find_by_id(event_id)

        # validate the participants
        # only validate or create participants in this portion. Participant should not be added
        # to event at this portion. Because at any loop, if one participant fails to be valid, others
        # that were previously added to the event would be useless
        for participant in data['participants']:
            # find the user
            participant_obj = ParticipantModel.find_by_email(
                participant['email'])

            # if exists, check if he has already participated in the event
            if participant_obj and participant_obj.has_participated_event(event_id):
                raise BadRequest(message='The email "{email}" is already registered under event "{event}"'.format(
                    email=participant['email'], event=event.name))
            elif participant_obj is None:
                # the participant does not exist, so create a new one
                self.create_participant(
                    participant['name'], participant['email'], participant['institute'])

        # at this point, all participants are valid.

        # create a team
        team = self.create_team(data['team_name'], event_id)

        # add participants to the corresponding team and event
        for participant in data['participants']:
            participant_obj = ParticipantModel.find_by_email(
                participant['email'])
            event.add_participant(participant_obj)
            team.add_participant(participant_obj)

        return TeamSchema(only=('id', 'name', 'team_identifier')).dump(team), 201

    def create_participant(self, name, email, institute):
        participant_obj = ParticipantModel(name, email, institute)
        participant_obj.save()
        return participant_obj

    def create_team(self, name, event_id):
        team = TeamModel(name, event_id)
        team.save()
        return team
