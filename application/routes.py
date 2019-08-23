from flask import current_app as app
from flask_restful import Api

from application.resources.event import Event, EventList, EventRegister
from application.resources.info import Info
from application.resources.participant import Participant
from application.resources.find import FindParticipant, FindEvent, FindTeam

# not used anywhere, but these imports are required to create the tables by sqlalchemy
from application.resources.event_participant import EventParticipant
from application.resources.team_participant import TeamParticipant


api = Api(app)

# root (to show basic information about the api)
api.add_resource(Info, '/')

# find entity by user readable data (like name, email etc)
api.add_resource(FindParticipant, '/find/participant')
api.add_resource(FindEvent, '/find/event/<string:name>')
api.add_resource(FindTeam, '/find/team')

# event create/remove and event listings
api.add_resource(EventList, '/events')
api.add_resource(Event, '/event/<string:name>')

# participants create/remove/update
api.add_resource(Participant, '/participant')

# event registration
api.add_resource(EventRegister, '/event/register/<int:event_id>')

