from flask import Blueprint, request
from controllers import transaction_controller

transaction = Blueprint("transaction", __name__)

@transaction.route('/transaction/add', methods=["POST"])
def add_transaction():
    return transaction_controller.add_transaction(request)

@transaction.route('/transaction/update/<id>', methods=["PUT"])
def update_transaction(id):
    return transaction_controller.update_transaction(request, id)

@transaction.route('/transactions', methods=['GET'])
def get_all_active_transactions():
    return transaction_controller.get_all_active_transactions(request)

@transaction.route("/transaction/<id>", methods=["GET"])
def get_transaction_by_id(id):
    return transaction_controller.get_transaction_by_id(request, id)

@transaction.route("/transaction/<id>", methods=["PATCH"])
def transaction_status(id):
    return transaction_controller.transaction_status(request, id)

@transaction.route('/transaction/delete/<id>', methods=["DELETE"])
def delete_transaction(id):
    return transaction_controller.delete_transaction(request, id)