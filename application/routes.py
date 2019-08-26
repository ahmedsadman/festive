from flask import current_app as app
from flask_restful import Api

from application.resources.event import EventCreate, EventList
from application.resources.event_register import EventRegister
from application.resources.team import FindTeam
from application.resources.info import Info
from application.resources.participant import Participant, FindParticipant

# not used anywhere, but these imports are required to create the tables by sqlalchemy
from application.tables import event_participant, team_participant

api = Api(app)

# root (to show basic information about the api)
api.add_resource(Info, '/')

# find entity by user readable data (like name, email etc)
api.add_resource(FindParticipant, '/find/participant')
api.add_resource(FindTeam, '/find/team')

# event create/remove and event listings
api.add_resource(EventCreate, '/event/create')
api.add_resource(EventList, '/events')

# event registration
api.add_resource(EventRegister, '/event/register/<int:event_id>')

