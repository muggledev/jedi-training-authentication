import uuid
from sqlalchemy.dialects.postgresql import UUID
from db import db
import marshmallow as ma


class Crystals(db.Model):
    __tablename__ = "Crystals"

    crystal_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    crystal_type = db.Column(db.String(), unique=True, nullable=False)
    origin_planet = db.Column(db.String(), nullable=False)
    rarity_level = db.Column(db.String(), nullable=False)
    force_amplify = db.Column(db.Float(), nullable=False)

    def __init__(self, crystal_type, origin_planet, rarity_level, force_amplify):
        self.crystal_type = crystal_type
        self.origin_planet = origin_planet
        self.rarity_level = rarity_level
        self.force_amplify = force_amplify

    def new_crystal_obj():
        return Crystals('', '', '', '')


class CrystalsSchema(ma.Schema):
    crystal_id = ma.fields.UUID()
    crystal_type = ma.fields.Str()
    origin_planet = ma.fields.Str()
    rarity_level = ma.fields.Str()
    force_amplify = ma.fields.Float()


crystal_schema = CrystalsSchema()
crystals_schema = CrystalsSchema(many=True)
