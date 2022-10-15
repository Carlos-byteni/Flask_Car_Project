from flask_restful import Resource
from modelo.person import PersonModel


class Person(Resource):
    """
    Class for making the abstract, validation and
    routes of the object persons.
    """

    def get(self, name):

        person = PersonModel.retrieve_name(name)
        if person is not None:
            return person.json()
        return {'message': 'Person not found'}, 404
    
    def post(self, name):

        if PersonModel.retrieve_name(name):
            return {'message': 'Person already exists'}, 400
        
        person = PersonModel(name)
        try:
            person.save()
        except:
            {'message': 'error generatin the person name'}, 500
        return person.json(), 201

    def delete(self, name):

        person = PersonModel.retrieve_name(name)
        if person:
            person.delete_db()
        return {'message': 'Person deleted'}
            
class PersonList(Resource):

    def get(self):
        return {'persons': [person.json() for person in PersonModel.query.all()]}