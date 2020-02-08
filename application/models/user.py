from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import check_password_hash, generate_password_hash

from application import db
from application.models import BaseModel


class UserModel(BaseModel):
    """The base user model, represents an admin in this case"""

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    _password = db.Column(db.String(150))
    email = db.Column(db.String(50), unique=True)
    super_admin = db.Column(db.Boolean, default=False)

    def __init__(self, username, password, email, super_admin=False):
        self.username = username
        self.password = password
        self.email = email
        self.super_admin = super_admin

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def reset_password(self, old_pass, new_pass):
        if self.check_password(old_pass):
            self.password = new_pass
            self.save()
            return True
        return False

    def is_super_admin(self):
        return self.super_admin is True
