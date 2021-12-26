from models import procedure
from app import db


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


def validate_on_create(procedure_info):
    errors = {}
    pass


def delete_procedure(procedure_id):
    procedure.Procedure.query.filter_by(id=procedure_id).delete()
    db.session.commit()
