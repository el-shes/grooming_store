import json
from service import jwt, master, user, procedure, breed
from flask import Response, abort
from flask_restful import Resource, reqparse
from models.reservation import reservation_schema, reservations_schema
from service import reservation, procedure
import datetime

reservation_post_args = reqparse.RequestParser()
reservation_post_args.add_argument("user", location='cookies')
reservation_post_args.add_argument("master_id")
reservation_post_args.add_argument("breed_id")
reservation_post_args.add_argument("procedure_id")
reservation_post_args.add_argument("date")
reservation_post_args.add_argument("time_from")
reservation_post_args.add_argument("time_to")

reservation_get_args = reqparse.RequestParser()
reservation_get_args.add_argument("user", location='cookies')


def validate_reservation_create(info):
    errors = reservation.validate_on_create_reservation(info)
    if errors:
        result = json.dumps(errors)
        abort(Response(result, 400))


class Reservation(Resource):

    def post(self):
        args = reservation_post_args.parse_args()
        client_decoded_token = jwt.decode(args["user"])
        client_id = client_decoded_token["id"]
        validate_reservation_create(args)
        final_price = round(procedure.compute_total_procedure_price(args["procedure_id"], args["breed_id"]))
        input_date = datetime.datetime.strptime(args["date"], '%d/%m/%Y').date()
        input_time_from = datetime.datetime.strptime(args["time_from"], '%H:%M').time()
        input_time_to = datetime.datetime.strptime(args["time_to"], '%H:%M').time()
        new_reservation = reservation.create_reservation(args["master_id"], client_id, args["breed_id"],
                                                         args["procedure_id"], input_time_from, input_time_to,
                                                         input_date, final_price)
        return new_reservation.id

    def get(self):
        args = reservation_get_args.parse_args()
        print(args["user"])
        user_decoded_token = jwt.decode(args["user"])
        reservations_query = reservation.get_reservations_by_user_id(user_decoded_token["id"])
        for rservation in reservations_query:
            mstr = master.get_master(rservation.master_id)
            usr = user.get_user(mstr.user_id)
            rservation.master_name = usr.first_name + " " + usr.last_name
            rservation.procedure_name = procedure.get_procedure(rservation.procedure_id).name
            rservation.breed_name = breed.get_breed(rservation.breed_id).name
        return reservations_schema.jsonify(reservations_query)


class ReservationById(Resource):

    def delete(self, reservation_id):
        reservation.delete_reservation(reservation_id)
