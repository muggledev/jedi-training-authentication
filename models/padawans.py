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


class PadawanSchema(ma.Schema):
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
