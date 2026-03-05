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
    simplefin_access_url = db.Column(db.String())
    last_sign_in = db.Column(db.DateTime, nullable=True)
    active = db.Column(db.Boolean(), default=True)

    roles = db.relationship("Roles", secondary=roles_users_association_table, back_populates="users")
    auth_tokens = db.relationship('AuthTokens', back_populates='user', cascade="all, delete")
    categories = db.relationship('Categories', back_populates='user')


class UsersSchema(ma.Schema):
    class Meta:
        fields = ['user_id', "username", 'first_name', 'last_name', 'email', 'simplefin_access_url', 'last_sign_in', 'active', "roles", "categories"]
    roles = ma.fields.List(ma.fields.String())
    categories = ma.fields.Nested('CategoriesSchema', many=True, exclude=('transaction',))

Users.schema = UsersSchema()
