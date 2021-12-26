from sqlalchemy.exc import SQLAlchemyError

from models import user
from app import db
import re


def create_user(first_name, last_name, password, role, phone):
    new_user = user.User(first_name, last_name, password, role, phone)
    db.session.add(new_user)
    db.session.commit()
    return new_user


def get_all():
    return user.User.query.all()


def update_user(user_id, first_name, last_name, role, phone):
    user_from_db = user.User.query.get(user_id)
    user_from_db.first_name = first_name
    user_from_db.last_name = last_name
    user_from_db.role = role
    user_from_db.phone = phone
    db.session.commit()
    return user_from_db


def get_user(user_id):
    return user.User.query.get(user_id)


def get_user_by_phone(user_phone):
    return user.User.query.filter_by(phone=user_phone).first()


def check_user_password(user, password):
    return user.check_password(password)


def validate_name(name, field_name, errors):
    if len(name) == 0:
        errors[field_name] = "Cannot be empty"
    elif re.fullmatch(r"[A-Za-z\s'-]+", name) is None:
        errors[field_name] = "Invalid symbol"


def validate_on_create(user_info):
    errors = {}
    if not user_info["phone"].isalnum() or len(user_info["phone"]) != 10:
        errors["phone"] = "Must contain numeric symbols and be of length 10"
    elif get_user_by_phone(user_info["phone"]) is not None:
        errors["phone"] = "User with this phone number already exists"
    if user.Role.value_of(user_info["role"]) is None:
        errors["role"] = "No such role"
    validate_name(user_info["first_name"], "first_name", errors)
    validate_name(user_info["last_name"], "last_name", errors)
    return errors


def delete_user(user_id):
    user.User.query.filter_by(id=user_id).delete()
    db.session.commit()
