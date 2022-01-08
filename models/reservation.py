from app import db, ma


# declaring Reservation Model


class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    master_id = db.Column(db.Integer, db.ForeignKey('master.id'))
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    breed_id = db.Column(db.Integer, db.ForeignKey('breed.id'))
    procedure_id = db.Column(db.Integer, db.ForeignKey('procedure.id'))
    time_from = db.Column(db.Time, nullable=False)
    time_to = db.Column(db.Time, nullable=False)
    date = db.Column(db.Date)
    final_price = db.Column(db.Integer)

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
