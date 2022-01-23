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
    all_slots_for_date = get_slots_by_master_id_and_date(master_id, date)
    all_reservations_for_date = reservation.get_reservations_by_master_id_and_date(master_id, date)
    procedure_duration = procedure.get_procedure(procedure_id).duration
    available_slots = calculate_available_slots(all_slots_for_date, all_reservations_for_date, procedure_duration)
    return available_slots


def get_slot_by_id(time_slot_id):
    return master_time_slot.MasterTimeSlot.query.get(time_slot_id)


def get_slots_by_master_id_and_date(master_id, date):
    return master_time_slot.MasterTimeSlot.query.filter_by(master_id=master_id, date=date).all()


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
                possible_slots.append({"start": possible_starting.strftime("%H:%M"),
                                       "end": possible_ending.strftime("%H:%M")})
            possible_starting = possible_starting + datetime.timedelta(minutes=30)
            possible_ending = possible_starting + datetime.timedelta(minutes=procedure_duration)
    return possible_slots


def validate_master_for_time_slot_creation(master_id):
    errors = {}
    if not master_id:
        errors["master_id"] = "Choose master first"
    elif master.get_master(master_id) is None:
        errors["master_id"] = "No such master"
    return errors


def time_slot_validation(time_from, time_to, date, master_id):
    start_work = convert_to_datetime(date, datetime.datetime.strptime('9:00', '%H:%M').time())
    end_work = convert_to_datetime(date, datetime.datetime.strptime('21:00', '%H:%M').time())
    time_from = convert_to_datetime(date, time_from)
    time_to = convert_to_datetime(date, time_to)
    current_date = datetime.datetime.now().date()
    errors = validate_master_for_time_slot_creation(master_id)
    if date < current_date:
        errors["date"] = "Can't put a time slot for past date"
    master_time_slots_for_a_day = get_slots_by_master_id_and_date(master_id, date)
    if time_from < start_work or time_from > (end_work - datetime.timedelta(minutes=30)):
        errors["time_from"] = "Slot should be placed from 9 to 20.30"
    else:
        is_valid_slot = True
        for master_time_slot_for_a_day in master_time_slots_for_a_day:
            master_time_slot_for_a_day_starting_hour = convert_to_datetime(date,
                                                                           master_time_slot_for_a_day.starting_hour)
            master_time_slot_for_a_day_ending_hour = convert_to_datetime(date, master_time_slot_for_a_day.ending_hour)
            if master_time_slot_for_a_day_starting_hour <= time_from < master_time_slot_for_a_day_ending_hour:
                is_valid_slot = False
        if not is_valid_slot:
            errors["time_from"] = "Slot with this starting time exists"
    if time_to > end_work or time_to < (start_work + datetime.timedelta(minutes=30)):
        errors["time_to"] = "Slot should be placed from 9.30 to 21"
    else:
        is_valid_slot = True
        for master_time_slot_for_a_day in master_time_slots_for_a_day:
            master_time_slot_for_a_day_starting_hour = convert_to_datetime(date,
                                                                           master_time_slot_for_a_day.starting_hour)
            master_time_slot_for_a_day_ending_hour = convert_to_datetime(date, master_time_slot_for_a_day.ending_hour)
            if master_time_slot_for_a_day_ending_hour >= time_to > master_time_slot_for_a_day_starting_hour:
                is_valid_slot = False
        if not is_valid_slot:
            errors["time_to"] = "Slot with this ending time exists"
    return errors


def is_slot_free_from_reservations(all_reservations_for_date, possible_ending, possible_starting):
    """
    Checks whether time slot is free and can be booked
    :param all_reservations_for_date: list of all reservations for a date
    :param possible_ending:
    :param possible_starting:
    :return:
    """
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

