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


def validate_on_create(procedure_info):

    pass


def delete_breed(breed_id):
    breed.Breed.query.filter_by(id=breed_id).delete()
    db.session.commit()
