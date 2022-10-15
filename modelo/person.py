from db import db


class PersonModel(db.Model):
    """
    Class for making the setting of the Person Model
    and the relationship between the cars id Database.
    """

    __tablename__ = 'persons'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    
    cars = db.relationship('CarModel', lazy='dynamic')
    

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'person_name': self.name, 'cars': [car.json() for car in self.cars.all()]}
    
    @classmethod
    def retrieve_name(cls, name):
        return cls.query.filter_by(name=name).first()
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_db(self):
        db.session.delete(self)
        db.session.commit()