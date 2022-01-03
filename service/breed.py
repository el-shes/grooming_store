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
    if digit_input is None:
        errors[field_name] = "Can't be blank"
    elif round(digit_input, 2) < 1.00:
        errors[field_name] = "Should be 1.00 or greater"
    elif isinstance(digit_input, int):
        errors[field_name] = "Should be decimal"
    elif not isinstance(digit_input, float):
        errors[field_name] = "Should be decimal"


def validate_on_create(breed_info):
    errors = {}
    if len(breed_info["name"]) == 0:
        errors["name"] = "Can't be blank"
    elif re.fullmatch(r"[A-Za-z ]+", breed_info["name"]) is None:
        errors["name"] = "Invalid symbol"
    elif get_breed_by_name(breed_info["name"]) is not None:
        errors["name"] = "Breed already exists"
    if len(breed_info["image_link"]) == 0:
        errors["image_link"] = "Can't be blank"
    validate_float_input(breed_info["fur_coefficient"], "fur_coefficient", errors)
    validate_float_input(breed_info["size_coefficient"], "size_coefficient", errors)
    return errors


def delete_breed(breed_id):
    breed.Breed.query.filter_by(id=breed_id).delete()
    db.session.commit()
