from marshmallow import Schema, fields


class EventSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Int()
    name = fields.Str(required=True)


class ParticipantSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Int()
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    institute = fields.Str(missing=None)
    events = fields.Pluck('EventSchema', 'name', many=True)
    teams = fields.List(fields.Nested('TeamSchema', only=('id', 'name')))


class TeamSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Str()
    name = fields.Str(required=True)
    event_id = fields.Int(required=True)
    payment_status = fields.Bool()
    team_identifier = fields.Str()

    # the 'teams' field should be excluded to avoid recursion error
    # because the field 'teams' itself is dependent on this TeamSchema
    team_members = fields.List(fields.Nested(
        'ParticipantSchema', exclude=('teams',), only=('id', 'name')))
    event = fields.Nested('EventSchema')


class EventRegistration(Schema):
    participants = fields.Nested(ParticipantSchema(
        only=('name', 'email', 'institute')), many=True)
    event_id = fields.Int()
