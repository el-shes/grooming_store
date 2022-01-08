from flask_restful import Resource, reqparse
from models.reservation import reservation_schema, reservations_schema


class Reservation(Resource):

    def post(self):
        pass
