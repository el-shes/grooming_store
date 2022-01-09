from models import reservation
from app import db


def create_reservation(master_id, client_id, breed_id, procedure_id, time_from, time_to, date, final_price):
    new_reservation = reservation.Reservation(master_id, client_id, breed_id, procedure_id,
                                              time_from, time_to, date, final_price)
    db.session.add(new_reservation)
    db.session.commit()
    return new_reservation


# def update_reservation(reservation_id, master_id, client_id, breed_id, procedure_id, time_from, time_to, date,
#                        final_price):
#     reservation_from_db = reservation.Reservation.query.get(reservation_id)
#
#     pass


def get_all():
    return reservation.Reservation.query.all()


def get_reservation_by_id(reservation_id):
    return reservation.Reservation.query.filter_by(id=reservation_id).first()


def get_reservations_by_user_id(user_id):
    return reservation.Reservation.query.filter_by(user_id=user_id)


def get_reservations_by_master_id_and_date(master_id, date):
    return reservation.Reservation.query.filter_by(master_id=master_id, date=date)


def delete_reservation(reservation_id):
    reservation.Reservation.query.filter_by(id=reservation_id).delete()
    db.session.commit()
