from flask import request, jsonify

from db import db
from models.accounts import account_schema, accounts_schema, Accounts
from util.reflection import populate_object
from lib.authenticate import auth

@auth
def add_account(request):
    req_data = request.form if request.form else request.get_json()

    if not req_data:
        return jsonify({"message" : "please enter all required fields"}), 400
    
    new_account = Accounts.new_account()

    populate_object(new_account, req_data)
    
    try:
        db.session.add(new_account)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message":"unable to create record"}), 400
    
    return jsonify({"message": "account created", "results": account_schema.dump(new_account)}), 201

@auth
def update_account(request, id):
    req_data = request.form if request.form else request.json
    existing_account = db.session.query(Accounts).filter(Accounts.account_id == id).first()

    if not existing_account:
        return jsonify({"message":"no existing account"})
    
    populate_object(existing_account, req_data)

    return jsonify({"message":"user updated", "results": account_schema.dump(existing_account)}), 201

@auth
def get_all_active_accounts(request):
    accounts = db.session.query(Accounts).all()

    if not accounts:
        return jsonify({"message": "no accounts exist"}), 404
    else:
        return jsonify({"message": "fetched accounts", "results": accounts_schema.dump(accounts)}), 200

@auth
def get_account_by_id(request, id):
    account = db.session.query(Accounts).filter(Accounts.account_id == id).first()

    if not account:
        return jsonify({"message": "account doesn't exist"}),404
    else:
        return jsonify({"message":"fetched account", "results": account_schema.dump(account)}), 200

@auth
def account_status(request, id):
    account_data = db.session.query(Accounts).filter(Accounts.account_id == id).first()

    if account_data:
        account_data.active = not account_data.active
        db.session.commit()

        return jsonify({"message":"changed status of account", "results": account_schema.dump(account_data)}), 200
    return jsonify({"message":"no account found"}), 404

@auth
def delete_account(request, id):
    account = db.session.query(Accounts).filter(Accounts.account_id == id).first()

    if not account:
        return jsonify({"message":"account doesn't exist"}), 404
    
    db.session.delete(account)
    db.session.commit()
    return jsonify({"message": "account deleted"}), 200