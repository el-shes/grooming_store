"""
declaring the Breed Model
"""
from sqlalchemy import Column, Integer, String, Float
from app import db, ma


class Breed(db.Model):
    __tablename__ = 'breed'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    fur_coefficient = Column(Float)
    size_coefficient = Column(Float)
    image_link = Column(String)

    def __init__(self, name, fur_coefficient, size_coefficient, image_link):
        self.name = name
        self.fur_coefficient = fur_coefficient
        self.size_coefficient = size_coefficient
        self.image_link = image_link


class BreedSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Breed


breed_schema = BreedSchema()
breeds_schema = BreedSchema(many=True)
