from app import db

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

    def __repr__(self):
        return "master's name = {}: client = {}, breed = {}," \
               " procedure = {}, from {} to {}, on {}. Final price = {}" \
               "".format(self.master_id, self.client_id, self.breed_id,
                         self.procedure_id,self.time_from, self.time_to, self.date, self.final_price)