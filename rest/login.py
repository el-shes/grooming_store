from flask_restful import Resource, reqparse
from flask import abort, make_response, Response
import json
from models.user import user_schema
from service import user, jwt, validation

user_post_args = reqparse.RequestParser()
user_post_args.add_argument('phone')
user_post_args.add_argument('password')

verify_post_args = reqparse.RequestParser()
verify_post_args.add_argument("token")


def validate_login_info(phone, password):
    errors = validation.validate_login(phone, password)
    if errors:
        result = json.dumps(errors)
        abort(Response(result, 400))


class Login(Resource):
    def post(self):
        args = user_post_args.parse_args()
        user_by_phone = user.get_user_by_phone(args["phone"])
        validate_login_info(user_by_phone, args["password"])
        user_token = jwt.encode(user_by_phone.id, user_by_phone.role)
        header = [('Set-Cookie', f'user={user_token}')]
        user_to_return = user_schema.jsonify(user_by_phone)
        return make_response(user_to_return, 200, header)


class Verify(Resource):
    def post(self):
        args = verify_post_args.parse_args()
        user_decoded_token = jwt.decode(args["token"])
        return user_decoded_token
