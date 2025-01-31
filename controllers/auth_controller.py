from flask import jsonify, request
from flask_bcrypt import check_password_hash

from db import db
from models.users import Users
from datetime import datetime, timedelta
from models.auth_tokens import AuthTokens, auth_token_schema
from lib.authenticate import auth

def cleanup_expired_tokens():
    """Remove all expired tokens from the database"""
    expired_tokens = (
        db.session.query(AuthTokens)
        .filter(AuthTokens.expiration < datetime.now())
        .all()
    )
    
    for token in expired_tokens:
        db.session.delete(token)
    
    db.session.commit()


def auth_token():
    cleanup_expired_tokens()

    token_req = request.get_json()

    fields = ['email', 'password']
    req_fields = ["email", "password"]

    values = {}

    for field in fields:
        field_data = token_req.get(field)
        values[field] = field_data
        if field in req_fields and not values[field]:
            return jsonify({"message": f'{field} is required'}), 401

    user_data = db.session.query(Users).filter(Users.email == values['email']).first()

    if not values['email'] or not values['password'] or not user_data:
        return jsonify({"message": "invalid login"}), 401

    valid_password = check_password_hash(user_data.password, values['password'])

    if not valid_password:
        return jsonify({"message": "invalid Login"}), 401

    existing_token = (
        db.session.query(AuthTokens)
        .filter(AuthTokens.user_id == user_data.user_id, AuthTokens.expiration > datetime.now())
        .first()
    )

    if existing_token:
        return jsonify({"message": {"auth_token": auth_token_schema.dump(existing_token)}}), 200

    expiry = datetime.now() + timedelta(hours=12)
    new_token = AuthTokens(user_data.user_id, expiry)
    db.session.add(new_token)
    db.session.commit()

    return jsonify({"message": {"auth_token": auth_token_schema.dump(new_token)}}), 201


@auth
def auth_token_remove(request, auth_info):
    if user_id is None:
        user_id = auth_info.user_id
        
    auth_data = db.session.query(AuthTokens).filter(AuthTokens.user_id == user_id).first()
    
    if auth_data:
        db.session.delete(auth_data)
        db.session.commit()
    
    return jsonify({"message" : "user logged out"}), 200

@auth
def delete_user_token(user_id):
    auth_data = db.session.query(AuthTokens).filter(AuthTokens.user.user_id == user_id).first()
    
    if auth_data:
        db.session.delete(auth_data)
        db.session.commit()
    return jsonify({"message" : "deleted auth token"})