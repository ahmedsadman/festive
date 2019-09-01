from sqlalchemy import func
from application import db
from application.error_handlers import ServerError


class BaseModel(db.Model):
    __abstract__ = True

    def save(self):
        '''save the item to database'''
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
    def find_query(cls, _filter):
        '''Build the query with the given level one filters (filters that has direct match with entity 
        attributes, not any nested relationship). Returns 'query' object'''
        query = cls.query
        exclude_lower = [int, bool]

        for attr, value in _filter.items():
            # func.lower doesn't work for INT/BOOL types in some production databases, so this should be properly handled
            # ex: lower(event.id) won't work because event.id is INT type
            # So the logic is, whenever the passed 'value' in this scope is INT, it means
            # we don't need to lower anything. Just compare the vanilla value
            _attr = getattr(cls, attr)
            _attr = _attr if (type(value) in exclude_lower) else func.lower(_attr)
            _value = value if (type(value) in exclude_lower) else func.lower(value)
            query = query.filter(_attr == _value)
        return query

    @classmethod
    def find(cls, _filter):
        '''find all entities by given filter'''
        return cls.find_query(_filter).all()
