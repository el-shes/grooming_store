from models import procedure
from service import breed
from app import db
import re


def compute_total_procedure_price(procedure_id, breed_id):
    basic_price = get_procedure(procedure_id).basic_price
    size_coefficient = breed.get_breed(breed_id).size_coefficient
    fur_coefficient = breed.get_breed(breed_id).fur_coefficient
    total_price = basic_price * size_coefficient * fur_coefficient
    return round(total_price)


def create_procedure(name, basic_price, duration):
    new_procedure = procedure.Procedure(name, basic_price, duration)
    db.session.add(new_procedure)
    db.session.commit()
    return new_procedure


def get_all():
    return procedure.Procedure.query.all()


def update_procedure(procedure_id, name, basic_price, duration):
    procedure_from_db = procedure.Procedure.query.get(procedure_id)
    procedure_from_db.name = name
    procedure_from_db.basic_price = basic_price
    procedure_from_db.duration = duration
    db.session.commit()
    return procedure_from_db


def get_procedure(procedure_id):
    return procedure.Procedure.query.get(procedure_id)


def get_procedure_by_name(name):
    return procedure.Procedure.query.filter_by(name=name).first()


def validate_number_inputs(digit_input, field_name, errors, max_amount):
    """
    Validating number inputs for create/update procedure
    :param digit_input: an input number
    :param field_name: name of field to check
    :param errors: dictionary with errors occurred on create/update
    :param max_amount: integer with max amount for field
    :return: dictionary of errors if any
    """
    if not isinstance(digit_input, int):
        errors[field_name] = "Should be a number"
    elif digit_input == 0:
        errors[field_name] = "Can't be zero"
    elif digit_input > max_amount:
        errors[field_name] = "Too long"


def basic_validation(procedure_info):
    """
    Basic info validation on create/update procedure
    :param procedure_info: dictionary of fields - info to validate
    :return: dictionary of errors if any
    """
    errors = {}
    if len(procedure_info["name"]) == 0:
        errors["name"] = "Can't be blank"
    elif re.fullmatch(r"[A-Za-z ]+", procedure_info["name"]) is None:
        errors["name"] = "Invalid symbol"
    validate_number_inputs(procedure_info["basic_price"], "basic_price", errors, 99999)
    validate_number_inputs(procedure_info["duration"], "duration", errors, 120)
    return errors


def validate_on_create(procedure_info):
    """
    Validating procedure name doesn't already exist on creation
    :param procedure_info: dictionary of fields - info to validate
    :return: dictionary of errors if any
    """
    errors = basic_validation(procedure_info)
    if get_procedure_by_name(procedure_info["name"]) is not None:
        errors["name"] = "Procedure already exists"
    return errors


def validate_on_update(procedure_info, procedure_id):
    """
    Validating id of procedure_name in procedure_info doesn't already exist in the database by procedure_id
    :param procedure_info:  dictionary of fields - info to validate
    :param procedure_id
    :return: dictionary of errors if any
    """
    errors = basic_validation(procedure_info)
    if errors:
        return errors
    procedure_by_name = get_procedure_by_name(procedure_info["name"])
    if procedure_by_name is not None and procedure_by_name.id != procedure_id:
        errors["name"] = "Procedure already exists"
    return errors


def delete_procedure(procedure_id):
    procedure.Procedure.query.filter_by(id=procedure_id).delete()
    db.session.commit()
