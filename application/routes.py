from flask import current_app as app
from flask_restful import Api

from application.resources.event import EventCreate, EventList, Event
from application.resources.event_register import EventRegister
from application.resources.team import FindTeam, Team
from application.resources.payment import Payment, PaymentVerify
from application.resources.info import Info
from application.resources.participant import FindParticipant, Participant

# not used anywhere, but these imports are required to create the tables by sqlalchemy
from application.tables import event_participant, team_participant

api = Api(app)

# root (to show basic information about the api)
api.add_resource(Info, '/')

# event create/remove and event listings
api.add_resource(EventCreate, '/event/create')
api.add_resource(Event, '/event/<int:event_id>')
api.add_resource(EventList, '/events')

# event registration
api.add_resource(EventRegister, '/event/register/<int:event_id>')

# participants
api.add_resource(Participant, '/participant/<int:participant_id>')

# teams
api.add_resource(Team, '/team/<int:team_id>')

# payment
api.add_resource(Payment, '/payment/<string:team_identifier>')
api.add_resource(PaymentVerify, '/payment/verify/<int:team_id>')

# find entity by user readable data (like name, email etc)
api.add_resource(FindParticipant, '/find/participant')
api.add_resource(FindTeam, '/find/team')

