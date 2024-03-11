from flask import jsonify, request
from flask_bcrypt import check_password_hash

from db import db
from models.users import Users
from datetime import datetime, timedelta
from models.auth_tokens import AuthTokens, auth_token_schema
from lib.authenticate import auth_with_return

def auth_token_add():
    token_request = request.json
    email = token_request.get("email")
    password = token_request.get("password")
    expiry = datetime.now() + timedelta(hours=12)
    user_data = db.session.query(Users). filter(Users.email == email). filter(Users.active).first()

    if not email or not password or not user_data:
        return jsonify({"message": "Invaild Login"}), 401
        
    valid_password = check_password_hash(user_data.password, password)

    if not valid_password:
        return jsonify({"message": "Invaild Login"}), 401

    existing_tokens = db.session.query(AuthTokens).filter(AuthTokens.user_id == user_data.user_id).all()

    if existing_tokens:
        for token in existing_tokens:
            if token.expiration < datetime.now():
                db.session.delete(token)

    new_token = AuthTokens(user_data.user_id, expiry)
    db.session.add(new_token)
    db.session.commit()

    return jsonify({"message" : {"auth_token": auth_token_schema.dump(new_token)}})

@auth_with_return
def auth_token_remove(request, auth_info):
    if user_id is None:
        user_id = auth_info.user_id
        
    auth_data = db.session.query(AuthTokens).filter(AuthTokens.user_id == user_id).first()
    
    if auth_data:
        db.session.delete(auth_data)
        db.session.commit()
    
    return jsonify("User Logged Out"), 200

# @auth
def delete_user_token(user_id):
    auth_data = db.session.query(AuthTokens).filter(AuthTokens.user_id == user_id).first()
    
    if auth_data:
        db.session.delete(auth_data)
        db.session.commit()