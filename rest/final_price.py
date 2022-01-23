from flask_restful import Resource
from service import procedure


class FinalPrice(Resource):

    def get(self, procedure_id, breed_id):
        final_price = procedure.compute_total_procedure_price(procedure_id, breed_id)
        return final_price
