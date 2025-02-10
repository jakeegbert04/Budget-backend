from flask import  Blueprint, request
from controllers import auth_controller

auth = Blueprint("auth", __name__)

@auth.route("/user/auth", methods=["POST"])
def auth_token():
    return auth_controller.auth_token()

@auth.route("/validate-session", methods=["GET"])
def validate_session():
    return auth_controller.validate_session()

@auth.route("/auth/check-login", methods=["get"])
def auth_check_login():
    return auth_controller.auth_check_login()

@auth.route("/logout", methods=["PUT"])
def auth_token_remove():
    return auth_controller.auth_token_remove(request)