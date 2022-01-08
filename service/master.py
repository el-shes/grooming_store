from models import master
from app import db


def create_master(user_id):
    new_master = master.Master(user_id)
    db.session.add(new_master)
    db.session.commit()
    return new_master


def set_stars(master_id, new_mark):
    found_master = master.Master.query.get(master_id)
    master_mark = found_master.stars
    number_of_marks = found_master.number_of_marks
    found_master.number_of_marks += 1
    average_mark = (master_mark * number_of_marks + new_mark) / found_master.number_of_marks
    found_master.stars = average_mark
    db.session.commit()
    return average_mark


def get_all():
    masters = master.Master.query.all()
    return masters


def get_all_from_list(ids):
    masters = []
    for master_id in ids:
        masters.append(get_master(master_id))
    return masters


def get_master_by_user_id(user_id):
    return master.Master.query.filter_by(user_id=user_id).first()


# possibly delete
def update_master(master_id, master_procedures):
    master_from_db = master.Master.query.get(master_id)
    master_from_db.master_procedures = master_procedures
    db.session.commit()
    return master_from_db


def get_master(master_id):
    found_master = master.Master.query.get(master_id)
    return found_master


def delete_master(master_id):
    master.Master.query.filter_by(id=master_id).delete()
    db.session.commit()
