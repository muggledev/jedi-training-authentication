import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from db import db
import marshmallow as ma


class AuthTokens(db.Model):
    __tablename__ = "AuthTokens"

    auth_token = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Users.user_id"), nullable=False)

    expiration_date = db.Column(db.DateTime(), nullable=False)


class AuthTokenSchema(ma.Schema):
    auth_token = ma.fields.UUID()
    user_id = ma.fields.UUID()
    expiration_date = ma.fields.DateTime()


auth_token_schema = AuthTokenSchema()
auth_tokens_schema = AuthTokenSchema(many=True)
