import uuid
from flask import jsonify, request, make_response
from flask_bcrypt import check_password_hash

from db import db
from models.users import Users, user_schema
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
    # cleanup_expired_tokens()
    token_req = request.get_json()
    
    fields = ['email', 'password']
    values = {field: token_req.get(field) for field in fields}

    for field in fields:
        if not values[field]:
            return jsonify({"message": f'{field} is required'}), 401

    user_data = db.session.query(Users).filter(Users.email == values['email']).first()
    if not user_data or not check_password_hash(user_data.password, values['password']):
        return jsonify({"message": "invalid login"}), 401

    # Get existing valid token
    existing_token = db.session.query(AuthTokens).filter(
        AuthTokens.user_id == user_data.user_id,
        AuthTokens.expiration > datetime.now()
    ).first()

    if existing_token:
        response = jsonify({"message": {"auth_token": auth_token_schema.dump(existing_token)}})
    else:
        
        expiry = datetime.now() + timedelta(hours=8)
        new_token = AuthTokens(user_id=user_data.user_id, expiration=expiry)
        new_token.auth_token = str(uuid.uuid4())
        db.session.add(new_token)
        db.session.commit()

        print("auth token", new_token.auth_token)
        response = make_response({"message": "Auth Success", "result": {"auth_info": auth_token_schema.dump(new_token), "user_info": user_schema.dump(user_data)}}, 201)
        response.set_cookie("_sid", new_token.auth_token, expires=new_token.expiration, httponly=True, samesite="None")
        return response
    return response, 201

def validate_session():
    retrieved_cookie = request.cookies.get('_sid')
    if not retrieved_cookie:
        return jsonify({"message": "No valid session"}), 401

    token_data = db.session.query(AuthTokens).filter(
        AuthTokens.auth_token == retrieved_cookie,
        AuthTokens.expiration > datetime.now()
    ).first()

    if not token_data:
        return jsonify({"message": "Invalid or expired session"}), 401

    return jsonify({"message": "Session valid", "user_id": token_data.user_id}), 200

# def validate_session():
#     auth_token = request.cookies.get("auth_token")
#     if not auth_token:
#         return jsonify({"message": "No valid session"}), 401

#     token_data = db.session.query(AuthTokens).filter(
#         AuthTokens.auth_token == auth_token,
#         AuthTokens.expiration > datetime.now()
#     ).first()

#     if not token_data:
#         return jsonify({"message": "Invalid or expired session"}), 401

#     return jsonify({"message": "Session valid", "user_id": token_data.user_id}), 200

@auth_with_return
def auth_check_login(self, auth_info):
    print(auth_info, "auth_info")
    # user_data = db.session.query(Users).filter(Users.user_id == auth_info.user.user_id).first()

    return jsonify({"message": "success", "results": {"auth_info": self.model.schema.dump(auth_info), "user_info": Users.schema.dump(user_data)}}), 200

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