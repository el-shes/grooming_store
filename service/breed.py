import re

from models import breed
from app import db


def create_breed(name, fur_coefficient, size_coefficient, image_link):
    new_breed = breed.Breed(name, fur_coefficient, size_coefficient, image_link)
    db.session.add(new_breed)
    db.session.commit()
    return new_breed


def get_all():
    breeds = breed.Breed.query.all()
    return breeds


def update_breed(breed_id, name, fur_coefficient, size_coefficient, image_link):
    breed_from_db = breed.Breed.query.get(breed_id)
    breed_from_db.name = name
    breed_from_db.fur_coefficient = fur_coefficient
    breed_from_db.size_coefficient = size_coefficient
    breed_from_db.image_link = image_link
    db.session.commit()
    return breed_from_db


def get_breed(breed_id):
    found_breed = breed.Breed.query.get(breed_id)
    return found_breed


def get_breed_by_name(name):
    found_breed = breed.Breed.query.filter_by(name=name).first()
    return found_breed


def validate_float_input(digit_input, field_name, errors):
    """
    Validation of number inputs of create/update procedure
    :param digit_input: number to validate
    :param field_name: name of number field
    :param errors: dictionary of errors occurred on create/update
    :return: dictionary of errors if any
    """
    if digit_input is None:
        errors[field_name] = "Can't be blank"
    elif not isinstance(digit_input, float):
        errors[field_name] = "Should be decimal"
    elif round(digit_input, 2) < 1.00:
        errors[field_name] = "Should be 1.00 or greater"


def basic_validation(breed_info):
    """
    Basic validation of the breed parameters passed on creation/update breed
    :param breed_info: dictionary of fields - info to validate
    :return: dictionary of errors if any
    """
    errors = {}
    if len(breed_info["name"]) == 0:
        errors["name"] = "Can't be blank"
    elif re.fullmatch(r"[A-Za-z ]+", breed_info["name"]) is None:
        errors["name"] = "Invalid symbol"
    if len(breed_info["image_link"]) == 0:
        errors["image_link"] = "Can't be blank"
    validate_float_input(breed_info["fur_coefficient"], "fur_coefficient", errors)
    validate_float_input(breed_info["size_coefficient"], "size_coefficient", errors)
    return errors


def validate_on_create(breed_info):
    errors = basic_validation(breed_info)
    if get_breed_by_name(breed_info["name"]) is not None:
        errors["name"] = "Breed already exists"
    return errors


def validate_on_update(breed_info, breed_id):
    errors = basic_validation(breed_info)
    breed_by_name = get_breed_by_name(breed_info["name"])
    if breed_by_name is not None and breed_by_name.id != breed_id:
        errors["phone"] = "User with this phone number already exists"
        return errors


def delete_breed(breed_id):
    breed.Breed.query.filter_by(id=breed_id).delete()
    db.session.commit()
