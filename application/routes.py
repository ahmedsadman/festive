from flask import current_app as app
from flask_restful import Api

from application.resources.event import Event, EventList
from application.resources.info import Info
from application.resources.participant import Participant
from application.resources.event_participant import EventParticipant
from application.resources.team import Team
from application.resources.team_participant import TeamParticipant
from application.resources.find import FindParticipant, FindEvent, FindTeam

api = Api(app)

# root (to show basic information)
api.add_resource(Info, '/')

# find entity by user readable data (like name, email etc)
api.add_resource(FindParticipant, '/find/participant/<string:email>')
api.add_resource(FindEvent, '/find/event/<string:name>')
api.add_resource(FindTeam, '/find/team')

# event create/remove and event listings
api.add_resource(EventList, '/events')
api.add_resource(Event, '/event/<string:name>')

# participants create/remove/update
api.add_resource(Participant, '/participant')

# teams creation and getting team info
api.add_resource(Team, '/team')

# map event and participant
api.add_resource(EventParticipant, '/participate')

# map team and participant
api.add_resource(TeamParticipant, '/member')
