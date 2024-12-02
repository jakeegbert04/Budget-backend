from flask import request, jsonify
from flask_bcrypt import generate_password_hash

from db import db
from models.transaction import transaction_schema, transactions_schema, Transaction
from util.reflection import populate_object
from lib.authenticate import auth

@auth
def add_transaction(request):
    req_data = request.form if request.form else request.get_json()

    if not req_data:
        return jsonify({"message" : "please enter all required fields"}), 400
    
    new_transaction = Transaction.new_transaction()

    populate_object(new_transaction, req_data)
    
    try:
        db.session.add(new_transaction)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message":"unable to create record"}), 400
    
    return jsonify({"message": "transaction created", "results": transaction_schema.dump(new_transaction)}), 201

@auth
def update_transaction(request, id):
    req_data = request.form if request.form else request.json
    existing_transaction = db.session.query(Transaction).filter(Transaction.transaction_id == id).first()

    if not existing_transaction:
        return jsonify({"message":"no existing transaction"})
    
    populate_object(existing_transaction, req_data)

    return jsonify({"message":"user updated", "results": transaction_schema.dump(existing_transaction)}), 201

@auth
def get_all_active_transactions(request):
    transactions = db.session.query(Transaction).all()

    if not transactions:
        return jsonify({"message": "no transactions exist"}), 404
    else:
        return jsonify({"message": "fetched transactions", "results": transactions_schema.dump(transactions)}), 200

@auth
def get_transaction_by_id(request, id):
    transaction = db.session.query(Transaction).filter(Transaction.transaction_id == id).first()

    if not transaction:
        return jsonify({"message": "transaction doesn't exist"}),404
    else:
        return jsonify({"message":"fetched transaction", "results": transaction_schema.dump(transaction)}), 200

@auth
def transaction_status(request, id):
    transaction_data = db.session.query(Transactions).filter(Transactions.transaction_id == id).first()

    if transaction_data:
        transaction_data.active = not transaction_data.active
        db.session.commit()

        return jsonify({"message":"changed status of transaction", "results": transaction_schema.dump(transaction_data)}), 200
    return jsonify({"message":"no transaction found"}), 404

@auth
def delete_transaction(request, id):
    transaction = db.session.query(Transactions).filter(Transactions.transaction_id == id).first()

    if not transaction:
        return jsonify({"message":"transaction doesn't exist"}), 404
    
    db.session.delete(transaction)
    db.session.commit()
    return jsonify({"message": "transaction deleted"}), 200