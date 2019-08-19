from marshmallow import Schema, fields


class EventSchema(Schema):
    id = fields.Int()
    name = fields.Str(required=True)


class ParticipantSchema(Schema):
    id = fields.Int()
    name = fields.Str(required=True)
    email = fields.Str(required=True)
    is_leader = fields.Bool(required=True)
    institute = fields.Str()
    events = fields.List(fields.Nested('EventSchema'))
    teams = fields.List(fields.Nested('TeamSchema', only=('id', 'name')))


class TeamSchema(Schema):
    id = fields.Str()
    name = fields.Str(required=True)
    event_id = fields.Int(required=True)
    payment_status = fields.Bool()
    team_identifier = fields.Str()

    # the 'teams' field should be excluded to avoid recursion error
    # because the field 'teams' itself is dependent on this TeamSchema
    team_members = fields.List(fields.Nested(
        'ParticipantSchema', exclude=('teams',), only=('id', 'name')))
