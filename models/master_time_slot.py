import uuid

from app import db, ma
from sqlalchemy import Column, String, Integer, Time, Date

"""declaring Master's time slot model"""


class MasterTimeSlot(db.Model):
    id = Column(String, primary_key=True)
    master_id = Column(Integer, db.ForeignKey('master.id'))
    date = Column(Date)
    starting_hour = Column(Time)
    ending_hour = Column(Time)

    def __init__(self, master_id, date, starting_hour, ending_hour):
        self.id = uuid.uuid1().hex
        self.master_id = master_id
        self.date = date
        self.starting_hour = starting_hour
        self.ending_hour = ending_hour


class MasterTimeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = MasterTimeSlot


master_time_schema = MasterTimeSchema()
masters_time_schema = MasterTimeSchema(many=True)
