from app import db, ma
from sqlalchemy import Column, Integer

# declaring Master's procedures Model


class MasterProcedure(db.Model):
    __tablename__ = 'master_procedure'
    __table_args__ = (
        db.PrimaryKeyConstraint('master_id', 'procedure_id'),
    )
    master_id = Column(Integer, db.ForeignKey('master.id'))
    procedure_id = Column(Integer, db.ForeignKey('procedure.id'))

    def __init__(self, master_id, procedure_id):
        self.master_id = master_id
        self.procedure_id = procedure_id


class ProcedureMasterSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = MasterProcedure


master_procedure_schema = ProcedureMasterSchema()
master_procedures_schema = ProcedureMasterSchema(many=True)
