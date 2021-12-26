from flask import Flask, request
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
CORS(app)
migrate = Migrate(app, db)

if __name__ == '__main__':

    from rest import breed as breed_rest
    from rest import procedure as produce_rest
    from rest import user as user_rest
    from rest import master as master_rest
    from rest import login as login_rest

    api.add_resource(login_rest.Login, '/login')

    api.add_resource(breed_rest.Breed, '/breed')
    api.add_resource(breed_rest.BreedById, '/breed/<int:breed_id>')

    api.add_resource(produce_rest.Procedure, '/procedure')
    api.add_resource(produce_rest.ProcedureById, '/procedure/<int:procedure_id>')

    api.add_resource(user_rest.User, '/user')
    api.add_resource(user_rest.UserById, '/user/<string:user_id>')

    api.add_resource(master_rest.Master, '/master')
    api.add_resource(master_rest.MasterById, '/<int:master_id>')

    app.run(debug=True)
