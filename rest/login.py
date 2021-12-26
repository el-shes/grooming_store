from flask_restful import Resource, reqparse
from service import user, jwt

user_post_args = reqparse.RequestParser()
user_post_args.add_argument('phone')
user_post_args.add_argument('password')


class Login(Resource):
    def post(self):
        args = user_post_args.parse_args()
        user_by_phone = user.get_user_by_phone(args['phone'])
        if user_by_phone is None:
            raise NameError
        is_correct_password = user.check_user_password(user_by_phone, args['password'])
        if not is_correct_password:
            raise ValueError
        user_token = jwt.encode(user_by_phone.id, user_by_phone.role)
        return user_token
