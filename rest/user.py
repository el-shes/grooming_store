import json
from flask import Response, abort
from flask_restful import Resource, reqparse

from models.user import user_schema, users_schema, Role
from service import user, master

user_post_args = reqparse.RequestParser()
user_post_args.add_argument("first_name", required=True)
user_post_args.add_argument("last_name", required=True)
user_post_args.add_argument("password")
user_post_args.add_argument("role")
user_post_args.add_argument("phone", required=True)


def validate_create_user_info(info):
    errors = user.validate_on_create(info)
    if errors:
        result = json.dumps(errors)
        abort(Response(result, 400))


def validate_update_user_info(info, user_id):
    errors = user.validate_on_update(info, user_id)
    if errors:
        result = json.dumps(errors)
        abort(Response(result, 400))


class User(Resource):

    def post(self):
        args = user_post_args.parse_args()
        if not args["password"]:
            args["password"] = "123"
        if not args["role"]:
            args["role"] = "CLIENT"
        validate_create_user_info(args)
        new_user = user.create_user(first_name=args["first_name"], last_name=args["last_name"],
                                    password=args["password"], role=args["role"], phone=args["phone"])
        if new_user.role == Role.MASTER:
            master.create_master(new_user.id)
        return user_schema.jsonify(new_user)

    def get(self):
        return users_schema.jsonify(user.get_all())


class UserById(Resource):

    def put(self, user_id):
        args = user_post_args.parse_args()
        validate_update_user_info(args, user_id)
        updated_user = user.update_user(user_id, first_name=args["first_name"], last_name=args["last_name"],
                                        role=args["role"], phone=args["phone"])
        return user_schema.jsonify(updated_user)

    def get(self, user_id):
        return user_schema.jsonify(user.get_user(user_id))

    def delete(self, user_id):
        user.delete_user(user_id)
