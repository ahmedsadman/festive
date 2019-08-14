from flask import current_app as app
from flask_restful import Api

from resources.event import Event, EventList
from resources.info import Info

api = Api(app)

# root
api.add_resource(Info, '/')

# event
api.add_resource(EventList, '/events')
api.add_resource(Event, '/event/<string:name>')
