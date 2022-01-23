import datetime

from models import reservation
from app import db
from service import jwt, master_time_slot


def create_reservation(master_id, client_id, breed_id, procedure_id, time_from, time_to, date, final_price):
    new_reservation = reservation.Reservation(master_id, client_id, breed_id, procedure_id,
                                              time_from, time_to, date, final_price)
    db.session.add(new_reservation)
    db.session.commit()
    return new_reservation


def get_all():
    return reservation.Reservation.query.all()


def get_reservation_by_id(reservation_id):
    return reservation.Reservation.query.filter_by(id=reservation_id).first()


def get_reservations_by_user_id(user_id):
    return reservation.Reservation.query.filter_by(client_id=user_id).all()


def get_reservations_by_master_id_and_date(master_id, date):
    return reservation.Reservation.query.filter_by(master_id=master_id, date=date).all()


def validate_on_create_reservation(reservation_info):
    errors = {}
    current_date = datetime.datetime.now().date()
    input_date = datetime.datetime.strptime(reservation_info["date"], '%d/%m/%Y').date()
    available_slots = master_time_slot.get_available_slots_for_procedure_on_date(input_date,
                                                                                 reservation_info["master_id"],
                                                                                 reservation_info["procedure_id"])
    lst_available_slots_time_from = [slot["start"] for slot in available_slots]
    lst_available_slots_time_to = [slot["end"] for slot in available_slots]
    client_id = jwt.decode(reservation_info["user"])["id"]
    if client_id is None:
        errors["user_id"] = "Not logged in"
    if reservation_info["master_id"] is None:
        errors["master_id"] = "Choose master"
    if reservation_info["procedure_id"] is None:
        errors["procedure_id"] = "Choose procedure"
    if reservation_info["breed_id"] is None:
        errors["breed_id"] = "Choose breed"
    if reservation_info["date"] is None:
        errors["date"] = "Pick a date"
    elif input_date < current_date:
        errors["date"] = "You can't make reservation for past date"
    if reservation_info["time_from"] is None:
        errors["time_from"] = "Pick suitable time"
    elif reservation_info["time_from"] not in lst_available_slots_time_from:
        errors["time_from"] = "Sorry. This time is not available"
    if reservation_info["time_to"] is None:
        errors["time_to"] = "Pick suitable time"
    elif reservation_info["time_to"] not in lst_available_slots_time_to:
        errors["time_to"] = "Sorry. This time is not available"
    return errors


def delete_reservation(reservation_id):
    reservation.Reservation.query.filter_by(id=reservation_id).delete()
    db.session.commit()
