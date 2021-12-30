import json
from flask import Response, abort
from flask_restful import Resource, reqparse

from models.procedure import procedure_schema, procedures_schema
from service import procedure, master_procedure

procedure_post_args = reqparse.RequestParser()
procedure_post_args.add_argument("name")
procedure_post_args.add_argument("basic_price")
procedure_post_args.add_argument("duration")
procedure_post_args.add_argument("master_ids", action="split")


def validate_procedure_info(info):
    errors = procedure.validate_on_create(info)
    if errors:
        result = json.dumps(errors)
        abort(Response(result, 400))


class Procedure(Resource):
    def post(self):
        args = procedure_post_args.parse_args()
        validate_procedure_info(args)
        new_procedure = procedure.create_procedure(name=args["name"], basic_price=args["basic_price"],
                                                   duration=args["duration"])
        if args["master_ids"] is not None:
            for master_id in args["master_ids"]:
                master_procedure.add_mapping(master_id, new_procedure.id)
        return procedure_schema.jsonify(new_procedure)

    def get(self):
        return procedures_schema.jsonify(procedure.get_all())


class ProcedureById(Resource):

    def put(self, procedure_id):
        args = procedure_post_args.parse_args()
        new_procedure = procedure.update_procedure(procedure_id, name=args["name"], basic_price=args["basic_price"],
                                                   duration=args["duration"])
        return procedure_schema.jsonify(new_procedure)

    #
    # def post(self, procedure_id):
    #     args = procedure_post_args.parse_args()
    #     all_masters_to_procedure = master_procedure.get_all_by_procedure_id(procedure_id)
    #     master_ids_from_request = args["master_ids"]
    #     for master_id in master_ids_from_request:
    #         if master_id not in all_masters_to_procedure:
    #             master_procedure.add_mapping(master_id, procedure_id)
    #     for master_id in all_masters_to_procedure:
    #         if master_id not in master_ids_from_request:
    #             master_procedure.del_mapping(master_id, procedure_id)
    #     return procedure_schema.jsonify(procedure.get_procedure(procedure_id))

    def get(self, procedure_id):
        return procedure_schema.jsonify(procedure.get_procedure(procedure_id))

    def delete(self, procedure_id):
        procedure.delete_procedure(procedure_id)
