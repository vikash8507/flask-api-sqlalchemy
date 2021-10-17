from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity

from models.user import UserModel


class UserResource(Resource):
    @jwt_required()
    def get(self):
        user = current_identity
        return {'user': {"id": user.id, "username": user.username}}, 200


class Register(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
            "username",
            type=str,
            required=True,
            help="Username required"
    )
    parser.add_argument(
            "password",
            type=str,
            required=True,
            help="Password required"
    )

    def post(self):
        data = Register.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': "User with this username is already exist"}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {'message': 'Registration successful'}, 201