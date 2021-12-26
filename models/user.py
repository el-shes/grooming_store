"""
declaring the User Model
"""
import enum
from sqlalchemy import Column, String
from app import db, ma
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.types import Enum
import uuid
from marshmallow import fields


class Role(enum.Enum):
    ADMIN = 'admin'
    MASTER = 'master'
    CLIENT = 'client'

    @classmethod
    def value_of(cls, name):
        for item_name, item in cls.__members__.items():
            if item_name == name:
                return item
        return None

    def __str__(self):
        return self.value


class User(db.Model):
    __tablename__ = 'user'
    id = Column(String, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(80))
    password = Column(String(128))
    role = Column(Enum(Role))
    phone = Column(String, index=True, unique=True, nullable=False)

    def __init__(self, first_name, last_name, password, role, phone):
        self.id = uuid.uuid1().hex
        self.first_name = first_name
        self.last_name = last_name
        self.password = generate_password_hash(password)
        self.role = role
        self.phone = phone

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class UserSchema(ma.SQLAlchemyAutoSchema):
    role = fields.Method("get_role")

    def get_role(self, obj):
        return obj.role.name

    class Meta:
        model = User
        exclude = ("password",)


user_schema = UserSchema(exclude=['password'])
users_schema = UserSchema(many=True)
