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

    def __init__(self, species_name, homeworld, forse_sensitive, avg_lifespan):
        self.species_name = species_name
        self.homeworld = homeworld
        self.forse_sensitive = forse_sensitive
        self.avg_lifespan = avg_lifespan

    def new_species_obj():
        return Species('', '', False, 0)

class SpeciesSchema(ma.Schema):
    class Meta:
        fields = ['species_id', 'species_name', 'homeworld', 'forse_sensitive', 'avg_lifespan']
    species_id = ma.fields.UUID()
    species_name = ma.fields.Str()
    homeworld = ma.fields.Str()
    forse_sensitive = ma.fields.Bool()
    avg_lifespan = ma.fields.Int()


species_schema = SpeciesSchema()
species_list_schema = SpeciesSchema(many=True)
