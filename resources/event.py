from flask_restful import Resource
from models.event import EventModel

class Event(Resource):
    def get(self, name):
        '''return details about the event with the given name'''
        event = EventModel.find_by_name(name)
        if event:
            return event.json()
        return {'message': 'Event not found'}, 404

    def post(self, name):
        '''create a new event with the given name'''
        # check if duplicate exists
        if EventModel.find_by_name(name):
            return {'message': 'The event with the name "{}" already exists'.format(name)}, 400

        event = EventModel(name)
        try:
            event.save()
            return event.json(), 201
        except:
            return {'message': 'Error occured while saving to db'}, 500

    def delete(self, name):
        event = EventModel.find_by_name(name)
        if event:
            event.delete()
        return {'message': 'Event deleted'}


class EventList(Resource):
    '''Handles list of events with specific information like number of participants'''
    def get(self):
        return {'events': [event.json() for event in EventModel.find_all()]}