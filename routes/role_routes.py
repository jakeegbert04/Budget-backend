from flask import request, Response, Blueprint
from controllers import roles_contoller

role = Blueprint("roles", __name__)


@role.route("/roles", methods=["GET"])
def get_all_roles() -> Response:
    return roles_contoller.get_all_roles(request)


@role.route("/role/<role_id>", methods=["GET"])
def get_role_by_id(role_id) -> Response:
    return roles_contoller.get_role_by_id(request, role_id)


@role.route("/role", methods=["POST"])
def add_role() -> Response:
    return roles_contoller.add_role(request)


@role.route("/role/<role_id>", methods=["PUT"])
def update_role(role_id) -> Response:
    return roles_contoller.update_role(request, role_id)


@role.route("/role/status/<role_id>", methods=["PATCH"])
def activate_deactivate_role(role_id) -> Response:
    return roles_contoller.activate_deactivate_role(request, role_id)


@role.route("/role/delete/<role_id>", methods=["DELETE"])
def delete_role(role_id) -> Response:
    return roles_contoller.delete_role(request, role_id)