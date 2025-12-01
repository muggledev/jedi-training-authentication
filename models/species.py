import uuid
from sqlalchemy.dialects.postgresql import UUID
from db import db
import marshmallow as ma


class Species(db.Model):
    __tablename__ = "Species"

    species_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    species_name = db.Column(db.String(), unique=True, nullable=False)
    homeworld = db.Column(db.String(), nullable=False)
    forse_sensitive = db.Column(db.Boolean(), nullable=False)
    avg_lifespan = db.Column(db.Integer(), nullable=False)


class SpeciesSchema(ma.Schema):
    species_id = ma.fields.UUID()
    species_name = ma.fields.Str()
    homeworld = ma.fields.Str()
    forse_sensitive = ma.fields.Bool()
    avg_lifespan = ma.fields.Int()


species_schema = SpeciesSchema()
species_list_schema = SpeciesSchema(many=True)
