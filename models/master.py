"""
declaring The Master Model
"""
from marshmallow import fields
from sqlalchemy import Column, Integer
from app import db, ma


class Master(db.Model):
    __tablename__ = 'master'
    # __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, db.ForeignKey('user.id'))
    stars = Column(Integer)
    number_of_marks = Column(Integer)
    # master_reservations = db.relationship('reservation')

    def __init__(self, user_id):
        self.user_id = user_id
        self.stars = None
        self.number_of_marks = 0


class MasterSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Master
        load_instance = True
        ordered = True
    name = fields.Method("get_name")

    def get_name(self, obj):
        if hasattr(obj, "name"):
            return obj.name
        return None


master_schema = MasterSchema()
masters_schema = MasterSchema(many=True)
