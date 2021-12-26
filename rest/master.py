from flask_restful import Resource, reqparse

from models.master import masters_schema, master_schema
from service import master, master_procedure

master_post_args = reqparse.RequestParser()
master_post_args.add_argument("user_id")
master_post_args.add_argument("stars")
master_post_args.add_argument("master_procedures")


class Master(Resource):

    def get(self):
        return masters_schema.jsonify(master.get_all())


class MasterById(Resource):

    # def post(self, master_id):
    #     args = master_post_args.parse_args()
    #     all_procedures_to_master = master_procedure.get_all_by_master_id(master_id)
    #     # procedure_ids_from_request = args["master_procedures"]
    #     # for procedure_id in procedure_ids_from_request:
    #     #     if procedure_id not in all_procedures_to_master:
    #     #         master_procedure.add_mapping(master_id, procedure_id)
    #     # for procedure_id in all_procedures_to_master:
    #     #     if procedure_id not in procedure_ids_from_request:
    #     #         master_procedure.del_mapping(master_id, procedure_id)
    #     return master_schema.jsonify(master.get_master(master_id))

    def put(self, master_id):
        args = master_post_args.parse_args()
        new_master = master.update_master(master_id, user_id=args["user_id"], stars=args["stars"],
                                          master_procedures=args["master_procedures"])
        return master_schema.jsonify(new_master)

    def get(self, master_id):
        return master_schema.jsonify(master.get_master(master_id))

    def delete(self, master_id):
        master.delete_master(master_id)
