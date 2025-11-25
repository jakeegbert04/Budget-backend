import uuid
from flask import jsonify, request, make_response
from flask_bcrypt import check_password_hash

from db import db
from models.users import Users
from datetime import datetime, timedelta
from models.auth_tokens import AuthTokens, auth_token_schema
from lib.authenticate import auth, auth_with_return

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
    token_req = request.get_json()
    
    fields = ['email', 'password']
    values = {field: token_req.get(field) for field in fields}

    for field in fields:
        if not values[field]:
            return jsonify({"message": f'{field} is required'}), 401

    user_data = db.session.query(Users).filter(Users.email == values['email']).first()
    if not user_data or not check_password_hash(user_data.password, values['password']):
        return jsonify({"message": "invalid login"}), 401

    existing_token = db.session.query(AuthTokens).filter(
        AuthTokens.user_id == user_data.user_id,
        AuthTokens.expiration > datetime.now()
    ).first()

    if existing_token:
        auth_token_data = auth_token_schema.dump(existing_token)
    else:
        expiry = datetime.now() + timedelta(hours=8)
        new_token = AuthTokens(user_id=user_data.user_id, expiration=expiry)
        new_token.auth_token = str(uuid.uuid4())
        db.session.add(new_token)
        db.session.commit()
        
        auth_token_data = auth_token_schema.dump(new_token)

    # Use the schema from the class
    response = make_response({
        "message": "Auth Success", 
        "results": {
            "auth_info": auth_token_data, 
            "user_info": Users.schema.dump(user_data)
        }
    }, 201)
    
    response.set_cookie(
        "auth_token", 
        auth_token_data["auth_token"],
        expires=datetime.now() + timedelta(hours=8),
        path="/",
        secure=True,
        httponly=True, 
        samesite="None", 
    )
    
    return response

def validate_session():
    retrieved_cookie = request.cookies.get('auth_token')
    
    if not retrieved_cookie:
        return jsonify({"authenticated": False, "message": "No valid session"}), 200

    token_data = db.session.query(AuthTokens).filter(
        AuthTokens.auth_token == retrieved_cookie,
        AuthTokens.expiration > datetime.now()
    ).first()

    if not token_data:
        return jsonify({"authenticated": False, "message": "Invalid or expired session"}), 200

    user_data = db.session.query(Users).filter(Users.user_id == token_data.user_id).first()
    
    if not user_data:
        return jsonify({"authenticated": False, "message": "User not found"}), 200

    return jsonify({
        "message": "Session Valid", 
        "results": Users.schema.dump(user_data)
    }), 200

@auth_with_return
def auth_token_remove(auth_info):
    auth_data = db.session.query(AuthTokens).filter(AuthTokens.user_id == auth_info.user_id).first()

    if auth_data:
        db.session.delete(auth_data)
        db.session.commit()

    response = make_response(jsonify({"message": "User logged out"}), 200)
    response.set_cookie("auth_token", "", expires=0, httponly=True, secure=True, samesite="None")

    return response

@auth
def delete_user_token(user_id):
    auth_data = db.session.query(AuthTokens).filter(AuthTokens.user_id == user_id).first()
    
    if auth_data:
        db.session.delete(auth_data)
        db.session.commit()
    return jsonify({"message": "deleted auth token"})