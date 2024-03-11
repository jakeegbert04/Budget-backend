from flask import Blueprint, request
from controllers import user_controller

user = Blueprint("user", __name__)
@user.route('/user/add', methods=["POST"])
def add_user():
    return user_controller.add_user(request)

@user.route('/user/update/<id>', methods=["PUT"])
def update_user(id):
    return user_controller.update_user(request, id)

@user.route('/users/get', methods=['GET'])
def get_all_active_users():
    return user_controller.get_all_active_users(request)

@user.route("/user/get/<id>", methods=["GET"])
def get_users_by_id(id):
    return user_controller.get_users_by_id(request, id)

@user.route("/user/status/<id>", methods=["PATCH"])
def user_status(id):
    return user_controller.user_status(request, id)

@user.route('/user/delete/<id>', methods=["DELETE"])
def delete_user(id):
    return user_controller.delete_user(request, id)