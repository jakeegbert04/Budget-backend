from flask import request, Response, Blueprint
from app import controllers

roles = Blueprint("roles", __name__)


@roles.route("/roles", methods=["GET"])
def get_all_roles() -> Response:
    return controllers.get_all_roles(request)


@roles.route("/role/<role_id>", methods=["GET"])
def get_role_by_id(role_id) -> Response:
    return controllers.get_role_by_id(request, role_id)


@roles.route("/role", methods=["POST"])
def add_role() -> Response:
    return controllers.add_role(request)


@roles.route("/role/<role_id>", methods=["PUT"])
def update_role(role_id) -> Response:
    return controllers.update_role(request, role_id)


@roles.route("/role/status/<role_id>", methods=["PATCH"])
def activate_deactivate_role(role_id) -> Response:
    return controllers.activate_deactivate_role(request, role_id)


@roles.route("/role/delete/<role_id>", methods=["DELETE"])
def delete_role(role_id) -> Response:
    return controllers.delete_role(request, role_id)