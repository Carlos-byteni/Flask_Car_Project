from db import db
from flask import Flask, request, jsonify
from flask_jwt_extended import create_access_token
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from flask_restful import Api

from logics.user import UserRegister
from logics.car import Car, CarList
from logics.person import Person, PersonList


app = Flask(__name__)
db.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = "super-secret"
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWTManager(app)

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if username != 'name' or password != '1234':
        return jsonify({'msg': "Bad username or password"}), 401
    
    access_token = create_access_token(identity=username)
    return jsonify(access_token)

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

api.add_resource(Car, '/car/<string:model>')
api.add_resource(CarList, '/cars')
api.add_resource(UserRegister, '/register')
api.add_resource(Person, '/person/<string:name>')
api.add_resource(PersonList,'/persons')
