import datetime
import json
from flask_restful import Resource, reqparse
from flask import abort, Response
from service import master_time_slot
from models.master_time_slot import master_time_schema


time_slot_post_args = reqparse.RequestParser()
time_slot_post_args.add_argument("master_id", required=True)
time_slot_post_args.add_argument("date", required=True)
time_slot_post_args.add_argument("starting_hour", required=True)
time_slot_post_args.add_argument("ending_hour", required=True)


def validate_time_slot_info(time_from, time_to, date, master_id):
    errors = master_time_slot.time_slot_validation(time_from, time_to, date, master_id)
    if errors:
        result = json.dumps(errors)
        abort(Response(result, 400))


class MasterTimeSlot(Resource):

    def post(self):
        args = time_slot_post_args.parse_args()
        date = datetime.datetime.strptime(args['date'], '%d/%m/%Y').date()
        time_from = datetime.datetime.strptime(args['starting_hour'], '%H:%M').time()
        time_to = datetime.datetime.strptime(args['ending_hour'], '%H:%M').time()
        validate_time_slot_info(time_from, time_to, date, args["master_id"])
        new_time_slot = master_time_slot.create_master_time_slot(master_id=args["master_id"], date=date,
                                                                 starting_hour=time_from,
                                                                 ending_hour=time_to)
        return master_time_schema.jsonify(new_time_slot)

    def get_available_slots(self, date, master_id, procedure_id):
        converted_date = datetime.datetime.strptime(date, '%d-%m-%Y').date()
        return master_time_schema.jsonify(
            master_time_slot.get_available_slots_for_procedure_on_date(converted_date, master_id, procedure_id))
