from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required

from modelo.cars import CarModel


class Car(Resource):
    """
    Class for making the abstract, validation and
    routes of the object cars.
    """

    parser = reqparse.RequestParser()
    parser.add_argument(
        'color', 
        type=str,
        required=True,
        help = 'This field must not be blank!'
    )
    parser.add_argument(
        'person_id', 
        type=int,
        required=True,
        help = 'Needed a person id field'
    )

    @jwt_required()
    def get(self, model):
        car = CarModel.retrieve_name(model)
        if car:
            return car.json()
        return {'massage': 'Car not found'}, 404

    def post(self, model):

        if CarModel.retrieve_name(model):
            return {'message': f'Car already exist with name {model}'}, 400

        data = Car.parser.parse_args()
        car = CarModel(model, data['color'], data['person_id'])
        
        car_model = car.json().get('model')
        car_color = car.json().get('color')

        if car_model != 'chevrolet' and car_model != 'volkswagen' and car_model != 'ford':
            return {
                'message': 'Permitted models only: chevrolet, volkswagen and ford'
            }
        if car_color != 'red' and car_color != 'blue' and car_color != 'black':
            return {
                'message': 'Permitted colors only: red, blue, black'
            }
        try:
            car.save()
        except:
            return {'massage': 'An error occurred.'}, 500
        return car.json(), 201

    @classmethod
    def delete(cls, model):
        car = CarModel.retrieve_name(model)
        if car:
            car.delete_db()
            return {'Messaga': 'car deleted'}, 200
        return {"message": "car not found"}, 404

    def put(self, model):
        data = Car.parser.parse_args()
        car = CarModel.retrieve_name(model)

        if car is None:
            car = CarModel(model, data['color'], data['person_id'])
        else:
            car.color = data['color']
        
        car_model = car.json().get('model')
        car_color = car.json().get('color')
        if car_model != 'chevrolet' and car_model != 'volkswagen' and car_model != 'ford':
            return {'message': 'Permitted models only: chevrolet, volkswagen and ford'}
        if car_color != 'red' and car_color != 'blue' and car_color != 'black':
            return {
                'message': 'Permitted colors only: red, blue, black'
            }
        car.save()
        return car.json()

class CarList(Resource):
    def get(self):
        return {'cars': [car.json() for car in CarModel.query.all()]}