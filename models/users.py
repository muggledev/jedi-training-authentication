import uuid
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID
from db import db
import marshmallow as ma


class Users(db.Model):
    __tablename__ = "Users"

    user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    temple_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Temples.temple_id"))

    username = db.Column(db.String(), unique=True, nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)

    password = db.Column(db.String(), nullable=False)

    force_rank = db.Column(db.String(), nullable=False)
    midi_count = db.Column(db.Integer(), nullable=False)

    is_active = db.Column(db.Boolean(), default=True)
    joined_date = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    def __init__(self, temple_id, username, email, password, force_rank, midi_count, is_active, joined_date):
        self.temple_id = temple_id
        self.username = username
        self.email = email
        self.password = password
        self.force_rank = force_rank
        self.midi_count = midi_count
        self.is_active = is_active
        self.joined_date = joined_date

    def new_user_obj():
        return Users('', '', '', '', '', 0, True, '')


class UsersSchema(ma.Schema):
    user_id = ma.fields.UUID()
    temple_id = ma.fields.UUID()
    username = ma.fields.Str()
    email = ma.fields.Str()
    force_rank = ma.fields.Str()
    midi_count = ma.fields.Int()
    is_active = ma.fields.Bool()
    joined_date = ma.fields.DateTime()


user_schema = UsersSchema()
users_schema = UsersSchema(many=True)
