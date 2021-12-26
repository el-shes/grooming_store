from models import master_procedure
from app import db


def add_mapping(master_id, procedure_id):
    mapping = master_procedure.MasterProcedure(master_id, procedure_id)
    db.session.add(mapping)
    db.session.commit()
    return mapping


def del_mapping(master_id, procedure_id):
    master_procedure.MasterProcedure.query.filter_by(procedure_id=procedure_id, master_id=master_id).delete()


def get_all_by_procedure_id(procedure_id):
    return master_procedure.MasterProcedure.query.filter_by(procedure_id=procedure_id).all()


def get_all_by_master_id(master_id):
    return master_procedure.MasterProcedure.query.filter_by(master_id=master_id).all()
