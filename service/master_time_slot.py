from models import master_time_slot
from app import db


def create_master_time_slot(master_id, date, starting_hour, ending_hour):
    new_master_time_slot = master_time_slot.MasterTimeSlot(master_id, date, starting_hour, ending_hour)
    db.session.add(new_master_time_slot)
    db.session.commit()
    return new_master_time_slot


def update_master_time_slot(time_slot_id, master_id, date, starting_hour, ending_hour):
    slot_from_db = master_time_slot.MasterTimeSlot.query.get(time_slot_id)
    slot_from_db.master_id = master_id
    slot_from_db.date = date
    slot_from_db.starting_hour = starting_hour
    slot_from_db.ending_hour = ending_hour
    db.session.commit()
    return slot_from_db


def get_all_slots():
    return master_time_slot.MasterTimeSlot.query.all()


def get_slot_by_id(time_slot_id):
    return master_time_slot.MasterTimeSlot.query.get(time_slot_id)


def delete_master_time_slot_by_id(time_slot_id):
    master_time_slot.MasterTimeSlot.query.filter_by(id=time_slot_id).delete()
    db.session.commit()
