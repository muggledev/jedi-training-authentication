import uuid
from sqlalchemy.dialects.postgresql import UUID
from db import db
import marshmallow as ma


class Temples(db.Model):
    __tablename__ = "Temples"

    temple_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    temple_name = db.Column(db.String(), unique=True, nullable=False)
    planet = db.Column(db.String(), nullable=False)

    master_count = db.Column(db.Integer(), nullable=False)
    padawan_limit = db.Column(db.Integer(), nullable=False)

    is_active = db.Column(db.Boolean(), default=True)

    def __init__(self, temple_name, planet, master_count, padawan_limit, is_active):
        self.temple_name = temple_name
        self.planet = planet
        self.master_count = master_count
        self.padawan_limit = padawan_limit
        self.is_active = is_active

    def new_temple_obj():
        return Temples('', '', 0, 0, True)


class TemplesSchema(ma.Schema):
    temple_id = ma.fields.UUID()
    temple_name = ma.fields.Str()
    planet = ma.fields.Str()
    master_count = ma.fields.Int()
    padawan_limit = ma.fields.Int()
    is_active = ma.fields.Bool()


temple_schema = TemplesSchema()
temples_schema = TemplesSchema(many=True)
