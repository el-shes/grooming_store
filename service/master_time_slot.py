from models import master_time_slot
from app import db
import datetime
from service import user, master, breed, procedure, reservation


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


def get_available_slots_for_procedure_on_date(date, master_id, procedure_id):
    all_slots_for_date = get_slot_by_master_id_and_date(master_id, date)
    all_reservations_for_date = reservation.get_reservations_by_master_id_and_date(master_id, date)
    procedure_duration = procedure.get_procedure(procedure_id).duration
    available_slots = calculate_available_slots(all_slots_for_date, all_reservations_for_date, procedure_duration)
    return available_slots


def get_slot_by_id(time_slot_id):
    return master_time_slot.MasterTimeSlot.query.get(time_slot_id)


def delete_master_time_slot_by_id(time_slot_id):
    master_time_slot.MasterTimeSlot.query.filter_by(id=time_slot_id).delete()
    db.session.commit()


def calculate_available_slots(all_slots_for_date, all_reservations_for_date, procedure_duration):
    possible_slots = []
    for slot in all_slots_for_date:
        possible_starting = convert_to_datetime(slot.date, slot.starting_hour)
        possible_ending = possible_starting + datetime.timedelta(minutes=procedure_duration)
        while slot.ending_hour.hour > possible_ending.hour or \
                (slot.ending_hour.hour == possible_ending.hour and slot.ending_hour.minute >= possible_ending.minute):
            is_valid_slot = is_slot_free_from_reservations(all_reservations_for_date, possible_ending,
                                                           possible_starting)
            if is_valid_slot:
                possible_slots.append({"start": possible_starting, "end": possible_ending})
            possible_starting = possible_starting + datetime.timedelta(minutes=30)
            possible_ending = possible_starting + datetime.timedelta(minutes=procedure_duration)
    return possible_slots


def is_slot_free_from_reservations(all_reservations_for_date, possible_ending, possible_starting):
    is_valid_slot = True
    for reserved_time in all_reservations_for_date:
        time_from = convert_to_datetime(reserved_time.date, reserved_time.time_from)
        time_to = convert_to_datetime(reserved_time.date, reserved_time.time_to)

        if time_from <= possible_starting < time_to or time_from < possible_ending <= time_to:
            is_valid_slot = False
            break
    return is_valid_slot


def convert_to_datetime(date, time):
    return datetime.datetime(year=date.year,
                             month=date.month,
                             day=date.day,
                             hour=time.hour, minute=time.minute)


def get_slot_by_master_id_and_date(master_id, date):
    return master_time_slot.MasterTimeSlot.query.filter_by(master_id=master_id, date=date)
