from flask import current_app as app
from flask_restful import Api

from resources.event import Event, EventList
from resources.info import Info
from resources.participant import Participant
from resources.event_participant import EventParticipant

api = Api(app)

# root (to show basic information)
api.add_resource(Info, '/')

# event create/remove and event listings
api.add_resource(EventList, '/events')
api.add_resource(Event, '/event/<string:name>')

# participants create/remove/update
api.add_resource(Participant, '/participant')

# map event and participant
api.add_resource(EventParticipant, '/participate')
