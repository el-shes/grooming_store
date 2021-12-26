from app import db

# declaring Master's time slot model


class MasterTimeSlot(db.Model):
    master_id = db.Column(db.Integer, db.ForeignKey('master.id'))
    date = db.Column(db.Date)
    starting_hour = db.Column(db.Time)
    ending_hour = db.Column(db.Time)

    def __repr__(self):
        return "Master {} works on {} from {} to {}".format(self.master_id, self.date,
                                                            self.starting_hour, self.ending_hour)
