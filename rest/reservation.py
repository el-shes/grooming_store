from service import jwt, master, user, procedure, breed
from flask_restful import Resource, reqparse
from models.reservation import reservation_schema, reservations_schema
from service import reservation
#
# reservation_post_args = reqparse.RequestParser()
# reservation_post_args.add_argument("token", location='cookie')
# reservation_post_args.add_argument("date")
# reservation_post_args.add_argument("time_from")
# reservation_post_args.add_argument("time_to")

#master_id, client_id, breed_id, procedure_id, time_from, time_to, date, final_price
reservation_get_args = reqparse.RequestParser()
reservation_get_args.add_argument("user", location='cookies')


class Reservation(Resource):

    def post(self):
        # args = reservation_post_args.parse_args()
        # client_decoded_token = jwt.decode(args["token"])

        pass

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
