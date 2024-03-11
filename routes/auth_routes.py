from flask import  Blueprint, request
from controllers import auth_controller

auth = Blueprint("auth", __name__)

@auth.route("/user/auth", methods=["POST"])
def auth_token_add():
    return auth_controller.auth_token_add()

@auth.route("/logout", methods=["PUT"])
def auth_token_remove():
    return auth_controller.auth_token_remove(request)