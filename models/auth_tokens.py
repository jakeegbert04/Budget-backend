import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID

from models.users import UsersSchema

from db import db

class AuthTokens(db.Model):
    __tablename__ = "AuthTokens"

    auth_token = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Users.user_id"), nullable=False)
    expiration = db.Column(db.DateTime, nullable=False)

    user = db.relationship('Users', back_populates='auth_tokens')


    def __init__(self, user_id, expiration):
        self.user_id = user_id
        self.expiration = expiration
        
class AuthTokenSchema(ma.Schema):
    class Meta:
        fields = ["auth_token", "user_id" "expiration", "user"]

    user = ma.fields.Nested(UsersSchema(only=("first_name", "last_name", "user_id", "email",)))

auth_token_schema = AuthTokenSchema()