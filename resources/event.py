from flask_restful import Resource
from models.event import EventModel
from application.error_handlers import *


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
            raise ServerError(message='Error occured while saving to db', error=e)

    def delete(self, name):
        event = EventModel.find_by_name(name)
        try:
            if event:
                event.delete()
            return {'message': 'Event deleted'}
        except Exception as e:
            raise ServerError(message='Error occured while trying to delete the item', error=e)


class EventList(Resource):
    '''Handles list of events with specific information like number of participants'''
    # number of participants not implemented yet
    def get(self):
        return {'events': [event.json() for event in EventModel.find_all()]}
