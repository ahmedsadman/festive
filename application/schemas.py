from marshmallow import Schema, fields, validates, validate, ValidationError


class EventSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Int()
    name = fields.Str(required=True)
    payable_amount = fields.Int(required=True)


class UserSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Int()
    username = fields.Str(required=True)
    password = fields.Str(required=True)


class ParticipantSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Int()
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    contact_no = fields.Str(required=False, missing=None)
    institute = fields.Str(missing=None)
    events = fields.Nested('EventSchema', only=('id', 'name'), many=True)
    teams = fields.Nested('TeamSchema', only=(
        'id', 'name', 'event_id'), many=True)


class PaymentSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Int()
    team_id = fields.Int()
    status = fields.Str()
    transaction_no = fields.Str(
        validate=[validate.Length(min=5), validate.Regexp('^[a-zA-Z0-9]+$')])
    created_on = fields.DateTime()
    updated_on = fields.DateTime()


class TeamSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Str()
    name = fields.Str(required=True)
    created_at = fields.DateTime()
    event_id = fields.Int(required=True)
    team_identifier = fields.Str()
    payment = fields.Nested('PaymentSchema', exclude=('id', 'team_id'))
    payment_status = fields.Str(load_only=True, validate=validate.OneOf(['pending', 'waiting', 'ok']))

    # the 'teams' field should be excluded to avoid recursion error
    # because the field 'teams' itself is dependent on this TeamSchema
    team_members = fields.List(fields.Nested(
        'ParticipantSchema', exclude=('teams',), only=('id', 'name')))
    event = fields.Nested('EventSchema', only=('id', 'name'))


class EventRegistration(Schema):
    participants = fields.Nested(ParticipantSchema(
        only=('name', 'email', 'institute')), many=True, required=True)
    team_name = fields.Str(required=True)

    @validates('participants')
    def validate_participants(self, value):
        if len(value) < 1:
            raise ValidationError(
                'At least one participant must exist in a team')
