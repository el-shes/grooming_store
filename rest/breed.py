import json

from flask_restful import Resource, reqparse
from flask import Response, abort
from models.breed import breed_schema, breeds_schema
from service import breed


breed_post_args = reqparse.RequestParser()
breed_post_args.add_argument("name")
breed_post_args.add_argument("fur_coefficient", type=float)
breed_post_args.add_argument("size_coefficient", type=float)
breed_post_args.add_argument("image_link")


def validate_create_breed_info(info):
    errors = breed.validate_on_create(info)
    if errors:
        result = json.dumps(errors)
        abort(Response(result, 400))


def validate_update_breed_info(info, breed_id):
    errors = breed.validate_on_update(info, breed_id)
    if errors:
        result = json.dumps(errors)
        abort(Response(result, 400))


class Breed(Resource):
    def post(self):
        args = breed_post_args.parse_args()
        validate_create_breed_info(args)
        new_breed = breed.create_breed(name=args["name"], fur_coefficient=args["fur_coefficient"],
                                       size_coefficient=args["size_coefficient"], image_link=args["image_link"])
        return breed_schema.jsonify(new_breed)

    def get(self):
        return breeds_schema.jsonify(breed.get_all())


class BreedById(Resource):

    def put(self, breed_id):
        args = breed_post_args.parse_args()
        validate_update_breed_info(args, breed_id)
        new_breed = breed.update_breed(breed_id, name=args["name"], fur_coefficient=args["fur_coefficient"],
                                       size_coefficient=args["size_coefficient"],  image_link=args["image_link"])
        return breed_schema.jsonify(new_breed)

    def get(self, breed_id):
        return breed_schema.jsonify(breed.get_breed(breed_id))

    def delete(self, breed_id):
        breed.delete_breed(breed_id)
