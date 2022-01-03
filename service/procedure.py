from models import procedure
from app import db
import re


def convert_to_cents(amount):
    return amount * 100


def create_procedure(name, basic_price, duration):
    new_procedure = procedure.Procedure(name, convert_to_cents(basic_price), duration)
    db.session.add(new_procedure)
    db.session.commit()
    return new_procedure


def get_all():
    return procedure.Procedure.query.all()


def update_procedure(procedure_id, name, basic_price, duration):
    procedure_from_db = procedure.Procedure.query.get(procedure_id)
    procedure_from_db.name = name
    procedure_from_db.basic_price = convert_to_cents(basic_price)
    procedure_from_db.duration = duration
    db.session.commit()
    return procedure_from_db


def get_procedure(procedure_id):
    return procedure.Procedure.query.get(procedure_id)


def get_procedure_id_by_name(name):
    return procedure.Procedure.query.filter_by(name=name).first()


def validate_number_inputs(digit_input, field_name, errors, max_digits_amount):
    if len(digit_input) == 0:
        errors[field_name] = "Can't be blank"
    elif not digit_input.isnumeric():
        errors[field_name] = "Should be a number"
    elif int(digit_input) == 0:
        errors[field_name] = "Can't be zero"
    elif len(digit_input) > max_digits_amount:
        errors[field_name] = "Too long"


def validate_on_create(procedure_info):
    errors = {}
    if len(procedure_info["name"]) == 0:
        errors["name"] = "Can't be blank"
    elif re.fullmatch(r"[A-Za-z ]+", procedure_info["name"]) is None:
        errors["name"] = "Invalid symbol"
    elif get_procedure_id_by_name(procedure_info["name"]) is not None:
        errors["name"] = "Procedure already exists"
    validate_number_inputs(procedure_info["basic_price"], "basic_price", errors, 5)
    validate_number_inputs(procedure_info["duration"], "duration", errors, 3)
    return errors


def delete_procedure(procedure_id):
    procedure.Procedure.query.filter_by(id=procedure_id).delete()
    db.session.commit()
