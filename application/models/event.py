from application import db


class EventModel(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    payable_amount = db.Column(db.Integer)

    teams = db.relationship('TeamModel', backref='event', lazy='dynamic')
    # participants -> backref from participant model

    def __init__(self, name, payable_amount):
        self.name = name
        self.payable_amount = payable_amount

    def save(self):
        '''save the item to database'''
        db.session.add(self)
        db.session.commit()

    def delete(self):
        '''delete the item from database'''
        db.session.delete(self)
        db.session.commit()

    def add_participant(self, participant):
        '''adds a participant under the event'''
        self.participants.append(participant)
        db.session.commit()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    # @classmethod
    # def find_participant(cls, email, event_id):
    #     '''find and return the participant if he has participated in a given event'''
    #     # return cls.query.filter_by(id=event_id).join(cls.participants).filter_by(email=email).first()
    #     event = cls.query.filter_by(id=event_id).first()
    #     return event.participants.filter_by(email=email).first()
