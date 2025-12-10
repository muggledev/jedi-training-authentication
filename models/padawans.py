import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from db import db
import marshmallow as ma


class Padawans(db.Model):
    __tablename__ = "Padawans"

    padawan_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    master_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Masters.master_id"))
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Users.user_id"))
    species_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Species.species_id"))

    padawan_name = db.Column(db.String(), unique=True, nullable=False)
    age = db.Column(db.Integer(), nullable=False)
    training_level = db.Column(db.Integer(), nullable=False)
    graduation_date = db.Column(db.DateTime())

    def __init__(self, master_id, user_id, species_id, padawan_name, age, training_level, graduation_date):
        self.master_id = master_id
        self.user_id = user_id
        self.species_id = species_id
        self.padawan_name = padawan_name
        self.age = age
        self.training_level = training_level
        self.graduation_date =graduation_date

    def new_padawan_obj():
        return Padawans(None, None, None, '', 0, 0, None)


class PadawanSchema(ma.Schema):
    class Meta:
        fields = ['padawan_id', 'master_id', 'user_id', 'species_id', 'padawan_name', 'age', 'training_level', 'graduation_date']
    padawan_id = ma.fields.UUID()
    master_id = ma.fields.UUID()
    user_id = ma.fields.UUID()
    species_id = ma.fields.UUID()
    padawan_name = ma.fields.Str()
    age = ma.fields.Int()
    training_level = ma.fields.Int()
    graduation_date = ma.fields.DateTime()


padawan_schema = PadawanSchema()
padawans_schema = PadawanSchema(many=True)
