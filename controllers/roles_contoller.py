from flask import jsonify, Request, Response

from db import db, query

from models.roles import Roles, roles_schema, role_schema
from lib.authenticate import auth

from util.validate_uuid import validate_uuid4
from util.reflection import populate_object


@auth
def get_all_roles(req: Request) -> Response:
    roles_query = query(Roles).all()

    return jsonify({"message": "roles", "results": roles_schema.dump(roles_query)}), 200


@auth
def get_role_by_id(req: Request, role_id) -> Response:

    if validate_uuid4(role_id) is False:
        return jsonify({"message": "invalid role id"}), 400

    role_data = query(Roles).filter(Roles.role_id == role_id).first()

    if role_data:
        return jsonify({"message": "role found", "results": role_schema.dump(role_data)}), 200

    return jsonify({"message": "role not found"}), 404


@auth
def add_role(req: Request) -> Response:

    post_data = req.form if req.form else req.json

    new_role = Roles.get_new_role()

    populate_object(new_role, post_data)

    db.session.add(new_role)
    db.session.commit()

    return jsonify({"message": "role added", "results": role_schema.dump(new_role)}), 201


@auth
def update_role(req: Request, role_id) -> Response:
    post_data = req.form if req.form else req.json

    if validate_uuid4(role_id) is False:
        return jsonify({"message": "invalid role id"}), 400

    role_query = query(Roles).filter(Roles.role_id == role_id).first()

    if role_query:
        if role_query.name == "super_admin":
            return jsonify({"message": "cannot update super admin"}), 403

        populate_object(role_query, post_data)
        db.session.commit()

        return jsonify({"message": "role updated", "results": role_schema.dump(role_query)}), 200

    return jsonify({"message": "role not found"}), 404


@auth
def activate_deactivate_role(reg: Request, role_id) -> Response:

    if validate_uuid4(role_id) is False:
        return jsonify({"message": "invalid role id"}), 400

    role_data = query(Roles).filter(Roles.role_id == role_id).first()

    if role_data:
        if role_data.name == "super_admin":
            return jsonify({"message": "cannot deactivate a super admin"}), 403

        role_data.active = not role_data.active
        db.session.commit()

        return jsonify({"message": "updated roles", "results": role_schema.dump(role_data)}), 200
    return jsonify({"message": "role not found"}), 404


@auth
def delete_role(req: Request, role_id) -> Response:

    if validate_uuid4(role_id) is False:
        return jsonify({"message": "invalid role id"}), 400

    role_data = query(Roles).filter(Roles.role_id == role_id).first()

    if role_data:
        if role_data.name == "super_admin":
            return jsonify({"message": "cannot delete a super admin"}), 403

        db.session.delete(role_data)
        db.session.commit()

        return jsonify({"message": "role deleted"}), 200

    return jsonify({"message": "role not found"}), 404