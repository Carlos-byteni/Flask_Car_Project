from db import db


class CarModel(db.Model):
    """
    Class for making the setting of the Car Model.
    and the relationship between the persons id Database.
    """

    __tablename__ = 'cars'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    color = db.Column(db.String(100))
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))
    person = db.relationship('PersonModel')

    def __init__(self, name, color, person_id):
        self.name = name
        self.color = color
        self.person_id = person_id

    def json(self):
        return {'model': self.name, 'color': self.color}
    
    @classmethod
    def retrieve_name(cls, model):
        return cls.query.filter_by(name=model).first()
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_db(self):
        db.session.delete(self)
        db.session.commit()
