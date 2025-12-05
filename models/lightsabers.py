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

    def __init__(self, owner_id, crystal_id, saber_name, hilt_material, blade_color, is_completed):
        self.owner_id = owner_id
        self.crystal_id = crystal_id
        self.saber_name = saber_name
        self.hilt_material = hilt_material
        self.blade_color = blade_color
        self.is_completed = is_completed

    def new_lightsaber_obj():
        return Lightsabers('', '', '', '', '', False)


class LightsabersSchema(ma.Schema):
    class Meta:
        fields = ['saber_id', 'owner_id', 'crystal_id', 'saber_name', 'hilt_material', 'blade_color', 'is_completed']
    saber_id = ma.fields.UUID()
    owner_id = ma.fields.UUID()
    crystal_id = ma.fields.UUID()
    saber_name = ma.fields.Str()
    hilt_material = ma.fields.Str()
    blade_color = ma.fields.Str()
    is_completed = ma.fields.Bool()


lightsaber_schema = LightsabersSchema()
lightsabers_schema = LightsabersSchema(many=True)
