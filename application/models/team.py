from application import db


class TeamModel(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    team_identifier = db.Column(db.String(50), nullable=True) # will handle later
    payment_status = db.Column(db.Boolean, default=False)

    # team_members -> backref from participant model
    # event -> backref from event model
    
    def __init__(self, name, event_id):
        self.name = name
        self.event_id = event_id

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'event_id': self.event_id,
            'payment_status': self.payment_status
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find(cls, **filter):
        '''find a team by it's name and event id'''
        return cls.query.filter_by(**filter).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()