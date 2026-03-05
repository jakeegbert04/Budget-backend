from flask import Blueprint
from controllers import simple_fin_controller

simple_fin = Blueprint("simple_fin", __name__)

@simple_fin.route("/bank/account", methods=["GET"])
def get_accounts():
    return simple_fin_controller.get_accounts()

@simple_fin.route("/bank/transactions", methods=["PUT"])
def get_transactions():
    return simple_fin_controller.get_transactions()

@simple_fin.route("/sort/transactions", methods=["POST"])
def sort_transactions():
    return simple_fin_controller.sort_transactions()