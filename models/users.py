import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db

from models.roles_users_xref import roles_users_association_table

class Users(db.Model):
    __tablename__ = "Users"

    user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(), nullable=False, unique=True )
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    active = db.Column(db.Boolean(), default=True)

    roles = db.relationship("Roles", secondary=roles_users_association_table, back_populates="users")
    auth_tokens = db.relationship('AuthTokens', back_populates='user', cascade="all, delete")


class UsersSchema(ma.Schema):
    class Meta:
        fields = ['user_id', "username", 'first_name', 'last_name', 'email', "active", "roles"]
    roles = ma.fields.List(ma.fields.String())

Users.schema = UsersSchema()
