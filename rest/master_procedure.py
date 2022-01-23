from flask_restful import Resource
from service import master_procedure, master
from models.master import masters_schema


class MasterProcedureById(Resource):

    def get(self, procedure_id):
        """
        gets all masters by procedure id
        """
        all_masters_ids_procedure_ids_by_procedure = master_procedure.get_all_by_procedure_id(procedure_id)
        master_ids = []
        for pairs in all_masters_ids_procedure_ids_by_procedure:
            master_ids.append(pairs.master_id)
        all_masters = master.set_masters_name(master.get_all_from_list(master_ids))
        return masters_schema.jsonify(all_masters)
