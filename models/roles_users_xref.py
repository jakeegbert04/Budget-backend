from db import db

roles_users_association_table = db.Table(
    "RolesUsersAssociation",
    db.Model.metadata,
    db.Column('role_id', db.ForeignKey('Roles.role_id'), primary_key=True),
    db.Column('user_id', db.ForeignKey('Users.user_id'), primary_key=True)
)