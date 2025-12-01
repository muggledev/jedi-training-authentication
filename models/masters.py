import uuid
from sqlalchemy.dialects.postgresql import UUID
from db import db
import marshmallow as ma


class Masters(db.Model):
    __tablename__ = "Masters"

    master_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Users.user_id"), nullable=False)

    master_name = db.Column(db.String(), unique=True, nullable=False)
    specialization = db.Column(db.String(), nullable=False)
    years_training = db.Column(db.Integer(), nullable=False)
    max_padawans = db.Column(db.Integer(), nullable=False)


class MastersSchema(ma.Schema):
    master_id = ma.fields.UUID()
    user_id = ma.fields.UUID()
    master_name = ma.fields.Str()
    specialization = ma.fields.Str()
    years_training = ma.fields.Int()
    max_padawans = ma.fields.Int()


master_schema = MastersSchema()
masters_schema = MastersSchema(many=True)
