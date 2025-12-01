import uuid
from sqlalchemy.dialects.postgresql import UUID
from db import db
import marshmallow as ma


class Lightsabers(db.Model):
    __tablename__ = "Lightsabers"

    saber_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    owner_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Users.user_id"))
    crystal_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Crystals.crystal_id"))

    saber_name = db.Column(db.String(), unique=True, nullable=False)
    hilt_material = db.Column(db.String(), nullable=False)
    blade_color = db.Column(db.String(), nullable=False)
    is_completed = db.Column(db.Boolean(), default=False)


class LightsabersSchema(ma.Schema):
    saber_id = ma.fields.UUID()
    owner_id = ma.fields.UUID()
    crystal_id = ma.fields.UUID()
    saber_name = ma.fields.Str()
    hilt_material = ma.fields.Str()
    blade_color = ma.fields.Str()
    is_completed = ma.fields.Bool()


lightsaber_schema = LightsabersSchema()
lightsabers_schema = LightsabersSchema(many=True)
