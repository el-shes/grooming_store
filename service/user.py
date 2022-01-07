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
    """
    Validate name inputs on create/update
    :param name: name input
    :param field_name: name of field to check
    :param errors: dictionary with errors occurred on create/update
    :return: dictionary with errors if any
    """
    if len(name) == 0:
        errors[field_name] = "Cannot be empty"
    elif re.fullmatch(r"[A-Za-z\s'-]+", name) is None:
        errors[field_name] = "Invalid symbol"


def basic_validation(user_info):
    """
    Basic info validation on create/update procedure
    :param user_info: dictionary of fields - info to validate
    :return: dictionary of errors if any
    """
    errors = {}
    if not user_info["phone"].isalnum() or len(user_info["phone"]) != 10:
        errors["phone"] = "Must contain numeric symbols and be of length 10"
    if user.Role.value_of(user_info["role"]) is None:
        errors["role"] = "No such role"
    validate_name(user_info["first_name"], "first_name", errors)
    validate_name(user_info["last_name"], "last_name", errors)
    return errors


def validate_on_create(user_info):
    """
    Validating user_phone doesn't already exist on creation
    :param user_info: dictionary of fields - info to validate
    :return: dictionary of errors if any
    """
    errors = basic_validation(user_info)
    if get_user_by_phone(user_info["phone"]) is not None:
        errors["phone"] = "User with this phone number already exists"
    return errors


def validate_on_update(user_info, user_id):
    """
    Validating id of user_phone in user_info doesn't already exist in the database by user_id
    :param user_info:  dictionary of fields - info to validate
    :param user_id
    :return: dictionary of errors if any
    """
    errors = basic_validation(user_info)
    if errors:
        return errors
    user_by_phone = get_user_by_phone(user_info["phone"])
    if user_by_phone is not None and user_by_phone.id != user_id:
        errors["phone"] = "User with this phone number already exists"
        return errors


def delete_user(user_id):
    user.User.query.filter_by(id=user_id).delete()
    db.session.commit()
