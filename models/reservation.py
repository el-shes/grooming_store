from app import db, ma
from sqlalchemy import Column, String, Integer, Time, Date
# declaring Reservation Model


class Reservation(db.Model):
    __tablename__ = 'reservation'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    master_id = Column(Integer, db.ForeignKey('master.id'))
    client_id = Column(Integer, db.ForeignKey('user.id'))
    breed_id = Column(Integer, db.ForeignKey('breed.id'))
    procedure_id = Column(Integer, db.ForeignKey('procedure.id'))
    time_from = Column(Time, nullable=False)
    time_to = Column(Time, nullable=False)
    date = Column(Date)
    final_price = Column(Integer)

    def __init__(self, master_id, client_id, breed_id, procedure_id, time_from, time_to, date, final_price):
        self.master_id = master_id
        self.client_id = client_id
        self.breed_id = breed_id
        self.procedure_id = procedure_id
        self.time_from = time_from
        self.time_to = time_to
        self.date = date
        self.final_price = final_price


class ReservationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Reservation


reservation_schema = ReservationSchema()
reservations_schema = ReservationSchema(many=True)
