from flask_restful import Resource, reqparse

from models.breed import breed_schema, breeds_schema
from service import breed


breed_post_args = reqparse.RequestParser()
breed_post_args.add_argument("name")
breed_post_args.add_argument("fur_coefficient")
breed_post_args.add_argument("size_coefficient")
breed_post_args.add_argument("image_link")


class Breed(Resource):
    def post(self):
        args = breed_post_args.parse_args()
        new_breed = breed.create_breed(name=args["name"], fur_coefficient=args["fur_coefficient"],
                                       size_coefficient=args["size_coefficient"], image_link=args["image_link"])
        return breed_schema.jsonify(new_breed)

    def get(self):
        return breeds_schema.jsonify(breed.get_all())


class BreedById(Resource):

    def put(self, breed_id):
        args = breed_post_args.parse_args()
        new_breed = breed.update_breed(breed_id, name=args["name"], fur_coefficient=args["fur_coefficient"],
                                       size_coefficient=args["size_coefficient"],  image_link=args["image_link"])
        return breed_schema.jsonify(new_breed)

    def get(self, breed_id):
        return breed_schema.jsonify(breed.get_breed(breed_id))

    def delete(self, breed_id):
        breed.delete_breed(breed_id)
