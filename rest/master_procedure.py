from flask_restful import Resource
from service import master_procedure, master
from models.master import masters_schema


class MasterProcedureById(Resource):

    def get_masters(self, procedure_id):
        """
        gets all masters by procedure id
        """
        all_masters_ids_by_procedure = master_procedure.get_all_by_procedure_id(procedure_id)
        all_masters = master.get_all_from_list(all_masters_ids_by_procedure)
        return masters_schema.jsonify(all_masters)
