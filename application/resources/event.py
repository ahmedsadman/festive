from flask import request
from flask_restful import Resource
from application.models.event import EventModel
from application.models.participant import ParticipantModel
from application.error_handlers import *
from application.schemas import EventRegistration


class Event(Resource):
    def get(self, name):
        '''return details about the event with the given name'''
        event = EventModel.find_by_name(name)
        if event:
            return event.json()
        raise NotFound()

    def post(self, name):
        '''create a new event with the given name'''
        # check if duplicate exists
        if EventModel.find_by_name(name):
            raise BadRequest(message='Event already exists')

        event = EventModel(name)
        try:
            event.save()
            return event.json(), 201
        except Exception as e:
            # this is server error, but the 'BadRequest' is used which might be confusing,
            # will keep it in this way for now. Later we can add something like 'ServerError' exception
            raise ServerError(
                message='Error occured while saving to db', error=e)

    def delete(self, name):
        event = EventModel.find_by_name(name)
        try:
            if event:
                event.delete()
            return {'message': 'Event deleted'}
        except Exception as e:
            raise ServerError(
                message='Error occured while trying to delete the item', error=e)


class EventList(Resource):
    '''Handles list of events with specific information like number of participants'''
    # number of participants not implemented yet

    def get(self):
        return {'events': [event.json() for event in EventModel.find_all()]}


class EventRegister(Resource):
    '''Handle event registrations for teams/participants'''

    def post(self, event_id):
        '''register participants under an event
        handles user creation, team creation and mapping in one place'''

        # parse data
        er_schema = EventRegistration()
        data = er_schema.load(request.get_json())
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
            if participant_obj and participant_obj.has_participated_event(data['event_id']):
                raise BadRequest(message='The email "{email}" is already registered under event "{event}"'.format(
                    email=participant['email'], event=event.name))
            elif participant_obj is None:
                # the participant does not exist, so create a new one
                self.create_participant(
                    participant['name'], participant['email'], participant['institute'])

        # at this point, all participants are valid.
        # add participants to the event
        for participant in data['participants']:
            participant_obj = ParticipantModel.find_by_email(
                participant['email'])
            event.add_participant(participant_obj)

        return {'message': 'Successfully added'}

    def create_participant(self, name, email, institute):
        participant_obj = ParticipantModel(name, email, institute)
        participant_obj.save()
