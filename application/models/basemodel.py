from sqlalchemy import func
from application import db
from application.error_handlers import ServerError


class BaseModel(db.Model):
    __abstract__ = True

    def save(self):
        '''delete the item from database'''
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            raise ServerError(message='Failed to save the item', error=e)

    def delete(self):
        '''delete the item from database'''
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            raise ServerError(message='Deletion failed', error=e)

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find(cls, _filter):
        '''find a team by given filter'''
        query = cls.query
        for attr, value in _filter.items():
            query = query.filter(func.lower(
                getattr(cls, attr)) == func.lower(value))
        return query.all()
