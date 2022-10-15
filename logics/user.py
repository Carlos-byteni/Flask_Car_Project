from flask_restful import Resource, reqparse
from modelo.user import UserModel

class UserRegister(Resource):
    """
    Class for making the abstract, routes and
    integration of the user register.
    """

    parser = reqparse.RequestParser()
    parser.add_argument(
        'username', 
        type=str,
        required=True,
        help = 'This field must be not blank!'
    )
    parser.add_argument(
        'password', 
        type=str,
        required=True,
        help = 'This field must be not blank!'
    )

    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.get_username(data['username']):
            return {'message': 'User with that username already exist'}, 400
        user = UserModel(data['username'], data['password']).save_to_db()
        return {'massage': f'User create successfully'}, 201
