from marshmallow import Schema, fields, validates, validate, validates_schema, ValidationError


class PaginatedResponse:
    '''Show paginated response in a proper format. Not an actual schema, because it will be
    only used to dump data.'''

    def __init__(self, paginated, schema):
        self.paginated = paginated
        self.items = schema.dump(self.paginated.items)

    def dump(self):
        if type(self.items) != list:
            raise ValidationError(
                'The schema should be a list object. Use many=True in schema')
        return {
            'total': self.paginated.total,
            'page': self.paginated.page,
            'has_prev': self.paginated.has_prev,
            'has_next': self.paginated.has_next,
            'data': self.items
        }


class BaseSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Int(dump_only=True)
    page = fields.Int(load_only=True)


class EventSchema(BaseSchema):
    name = fields.Str(required=True)
    payable_amount = fields.Int(required=True)
    payable_school = fields.Int(missing=None)
    payable_college = fields.Int(missing=None)
    payable_university = fields.Int(missing=None)


class UserSchema(BaseSchema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)


class ParticipantSchema(BaseSchema):
    name = fields.Str(required=True, validate=validate.Length(max=60))
    email = fields.Email(required=True, validate=validate.Length(max=60))
    contact_no = fields.Str(missing=None, validate=validate.Length(max=30))
    institute = fields.Str(missing=None, validate=validate.Length(max=60))
    tshirt_size = fields.Str(missing=None, validate=validate.OneOf(['s', 'm', 'l', 'xl', 'xxl']))
    events = fields.Nested('EventSchema', only=('id', 'name'), many=True)
    event_id = fields.Int(dump_only=True)
    teams = fields.Nested('TeamSchema', only=(
        'id', 'name', 'event_id'), many=True)


class PaymentSchema(BaseSchema):
    team_id = fields.Int()
    status = fields.Str()
    transaction_no = fields.Str(
        validate=[validate.Length(min=5), validate.Regexp('^[a-zA-Z0-9]+$')])
    created_on = fields.DateTime()
    updated_on = fields.DateTime()


class TeamSchema(BaseSchema):
    name = fields.Str(required=True)
    single = fields.Bool()
    participation_level = fields.Str(dump_only=True)
    created_at = fields.DateTime()
    event_id = fields.Int(required=True)
    team_identifier = fields.Str()
    payment = fields.Nested('PaymentSchema', exclude=('id', 'team_id'))
    payment_status = fields.Str(
        dump_only=True, validate=validate.OneOf(['pending', 'waiting', 'ok']))

    # the 'teams' field should be excluded to avoid recursion error
    # because the field 'teams' itself is dependent on this TeamSchema
    team_members = fields.List(fields.Nested(
        'ParticipantSchema', exclude=('teams',), only=('id', 'name')))
    event = fields.Nested('EventSchema', only=('id', 'name'))


class EventRegistration(BaseSchema):
    participants = fields.Nested(ParticipantSchema(
        only=('name', 'email', 'institute', 'tshirt_size')), many=True, required=True)
    team_name = fields.Str(required=True, validate=validate.Length(max=50))
    participation_level = fields.Str(missing=None,
                                     validate=validate.OneOf(['university', 'school', 'college']))
    single = fields.Bool(required=True)

    @validates('participants')
    def validate_participants(self, value):
        if len(value) == 0:
            raise ValidationError(
                'At least one participant must exist in a team')

    @validates_schema
    def check_single(self, data, **kwargs):
        '''validate that 'single' field is consistent with participant length'''
        if data['single'] and len(data['participants']) > 1:
            raise ValidationError(
                'Only one participant should exist when single=True')
