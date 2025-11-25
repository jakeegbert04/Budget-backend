import uuid
import marshmallow as ma
from sqlalchemy.dialects.postgresql import UUID

from db import db

from models.roles_users_xref import roles_users_association_table


class Roles(db.Model):
    __tablename__ = "Roles"
    role_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = db.Column(db.String(), nullable=False)
    active = db.Column(db.Boolean(), nullable=False, default=True)

    users = db.relationship("Users", secondary=roles_users_association_table, back_populates="roles")

class RolesSchema(ma.Schema):
    class Meta:
        fields = ['role_id', 'name', 'active']

Roles.schema = RolesSchema()