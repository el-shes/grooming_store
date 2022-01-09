import datetime

from flask_restful import Resource, reqparse
from service import master_time_slot
from models.master_time_slot import master_time_schema, masters_time_schema


time_slot_post_args = reqparse.RequestParser()
time_slot_post_args.add_argument("master_id", required=True)
time_slot_post_args.add_argument("date", required=True)
time_slot_post_args.add_argument("starting_hour", required=True)
time_slot_post_args.add_argument("ending_hour", required=True)


class MasterTimeSlot(Resource):

    def post(self):
        args = time_slot_post_args.parse_args()
        new_time_slot = master_time_slot.create_master_time_slot(master_id=args["master_id"], date=args["date"],
                                                                 starting_hour=args["starting_hour"],
                                                                 ending_hour=args["ending_hour"])
        return master_time_schema.jsonify(new_time_slot)

    def get_available_slots(self, date, master_id, procedure_id):
        converted_date = datetime.datetime.strptime(date, '%d-%m-%Y').date()
        return master_time_schema.jsonify(
            master_time_slot.get_available_slots_for_procedure_on_date(converted_date, master_id, procedure_id))
