import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db

class Users(db.Model):
    __tablename__ = "Users"

    user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(), nullable=False, unique=True )
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    active = db.Column(db.Boolean(), default=True)

    def __init__(self, first_name, last_name, email, password, active):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.active = active

    def new_user():
        return Users( "", "", "", "", True)

class UsersSchema(ma.Schema):
    class Meta:
        fields = ['user_id', 'first_name', 'last_name', 'email', 'role', 'phone', 'is_photographer', 'bio', 'about_me', 'active', 'links_xref', 'comments_xref']
    links_xref = ma.fields.Nested("LinksXrefSchema", many=True)
    comments_xref = ma.fields.Nested("CommentsXrefSchema", many=True)

user_schema = UsersSchema()
users_schema = UsersSchema(many=True)