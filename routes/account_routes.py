from flask import Blueprint, request
from controllers import account_controller

account = Blueprint("account", __name__)

@account.route('/account/add', methods=["POST"])
def add_account():
    return account_controller.add_account(request)

@account.route('/account/update/<id>', methods=["PUT"])
def update_account(id):
    return account_controller.update_account(request, id)

@account.route('/accounts', methods=['GET'])
def get_all_active_accounts():
    return account_controller.get_all_active_accounts(request)

@account.route("/account/<id>", methods=["GET"])
def get_account_by_id(id):
    return account_controller.get_account_by_id(request, id)

@account.route("/account/<id>", methods=["PATCH"])
def account_status(id):
    return account_controller.account_status(request, id)

@account.route('/account/delete/<id>', methods=["DELETE"])
def delete_account(id):
    return account_controller.delete_account(request, id)