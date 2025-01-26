from flask import request, jsonify
from flask_bcrypt import generate_password_hash

from db import db
from models.transactions import transaction_schema, transactions_schema, Transactions
from models.users import Users
from models.categories import Categories
from util.reflection import populate_object
from lib.authenticate import auth

@auth
def add_transaction(request):
    req_data = request.form if request.form else request.get_json()

    user_id = req_data["user_id"]
    category_id = req_data["category_id"]
    amount = req_data["amount"]

    if not req_data:
        return jsonify({"message" : "please enter all required fields"}), 400
    
    user_id_qury = db.session.query(Users).filter(Users.user_id == user_id).first()

    if not user_id_qury:
        return jsonify({"message" : "user not found"}), 401
    
    category_id_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    if not category_id_query:
        return jsonify({"message" : "category not found"}), 401
    
    category_id_query.amount = int(category_id_query.amount) - int(amount)

    new_transaction = Transactions.new_transaction()


    populate_object(new_transaction, req_data)
    
    db.session.add(new_transaction)
    db.session.commit()
    
    return jsonify({"message": "transaction created", "results": transaction_schema.dump(new_transaction)}), 201

@auth
def update_transaction(request, id):
    req_data = request.form if request.form else request.json
    existing_transaction = db.session.query(Transactions).filter(Transactions.transaction_id == id).first()

    if not existing_transaction:
        return jsonify({"message":"no existing transaction"})
    
    populate_object(existing_transaction, req_data)

    return jsonify({"message":"user updated", "results": transaction_schema.dump(existing_transaction)}), 201

@auth
def get_all_active_transactions(request):
    transactions = db.session.query(Transactions).all()

    if not transactions:
        return jsonify({"message": "no transactions exist"}), 404
    else:
        return jsonify({"message": "fetched transactions", "results": transactions_schema.dump(transactions)}), 200

@auth
def get_transaction_by_id(request, id):
    transaction = db.session.query(Transactions).filter(Transactions.transaction_id == id).first()

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