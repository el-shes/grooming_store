from models import reservation
from app import db


def create_reservation(master_id, client_id, breed_id, procedure_id, time_from, time_to, date, final_price):
    new_reservation = reservation.Reservation(master_id, client_id, breed_id, procedure_id,
                                              time_from, time_to, date, final_price)
    db.session.add(new_reservation)
    db.session.commit()
    return new_reservation

def update_reservation(reservation_id, master_id, client_id, breed_id, procedure_id, time_from, time_to, date, final_price):
    pass

def get_all():
    pass

def get_reservation_by_id():
    pass

def delete_reservation():
    pass
