from config import roles_data
from db import db, query

from models.roles import Roles


def add_roles():
    for role in roles_data:
        new_role = query(Roles).filter(Roles.name == role).first()

        if new_role == None:
            name = role
            active = True
            new_role = Roles(name=name, active=active)

            db.session.add(new_role)

    db.session.commit()