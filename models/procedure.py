from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import dynamic

from app import db, ma


class Procedure(db.Model):
    """
    declaring the Procedure Model
    """
    __tablename__ = 'procedure'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    basic_price = Column(Integer)
    duration = Column(Integer)
    # procedure_reservations = db.relationship('reservation')

    def __init__(self, name, basic_price, duration):
        self.name = name
        self.basic_price = basic_price
        self.duration = duration


class ProcedureSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Procedure


procedure_schema = ProcedureSchema()
procedures_schema = ProcedureSchema(many=True)
