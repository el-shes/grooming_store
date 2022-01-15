from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api
from flask_cors import CORS
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # to supress warnings
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)
cors = CORS(app, support_credentials=True)
migrate = Migrate(app, db)

if __name__ == '__main__':

    from rest import breed as breed_rest
    from rest import procedure as procedure_rest
    from rest import user as user_rest
    from rest import master as master_rest
    from rest import login as login_rest
    from rest import reservation as reservation_rest
    from rest import master_procedure as master_procedure_rest
    from rest import master_time_slots as time_slot_rest

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,OPTIONS,PUT,POST,DELETE')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Content-Type', 'application/json')
        if 'Access-Control-Allow-Origin' not in response.headers:
            response.headers.add('Access-Control-Allow-Origin', 'http://127.0.0.1:3000')
        return response

    api.add_resource(login_rest.Login, '/login')
    api.add_resource(login_rest.Verify, '/verify')

    api.add_resource(breed_rest.Breed, '/breed')
    api.add_resource(breed_rest.BreedById, '/breed/<int:breed_id>')

    api.add_resource(procedure_rest.Procedure, '/procedure')
    api.add_resource(procedure_rest.ProcedureById, '/procedure/<int:procedure_id>')

    api.add_resource(user_rest.User, '/user')
    api.add_resource(user_rest.UserById, '/user/<string:user_id>')

    api.add_resource(master_rest.Master, '/master')
    api.add_resource(master_rest.MasterById, '/master/<int:master_id>')
    api.add_resource(master_procedure_rest.MasterProcedureById, '/master/procedure/<int:procedure_id>')

    api.add_resource(time_slot_rest.MasterTimeSlot, '/time-slot')

    api.add_resource(reservation_rest.Reservation, '/reservation')
    api.add_resource(reservation_rest.ReservationById, '/reservation/<int:reservation_id>')

    app.run(debug=True)
