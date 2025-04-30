import functools
from flask import jsonify, request
from datetime import datetime
from uuid import UUID

from db import db
from models.auth_tokens import AuthTokens


def validate_uuid4(uuid_string):
    try:
        UUID(uuid_string, version=4)
        return True
    except:
        return False

def validate_token(req):
    if not req:
        req = request
    
    if 'auth_token' not in req.headers:
        return False
        
    auth_token = req.headers['auth_token']

    if not auth_token or not validate_uuid4(auth_token):
        return False

    existing_token = db.session.query(AuthTokens).filter(AuthTokens.auth_token == auth_token).first()

    if existing_token:
        if existing_token.expiration > datetime.now():
            return existing_token
    else:
        return False

def fail_response():
    return jsonify({"message": "authentication required"}), 401

def auth(func):
    @functools.wraps(func)
    def wrapper_auth_return(*args, **kwargs):
        auth_info = validate_token(args[0] if args else None)

        if auth_info:
            return func(*args, **kwargs)
        else:
            return fail_response()
    return wrapper_auth_return

def auth_with_return(func):
    @functools.wraps(func)
    def wrapper_auth_return(*args, **kwargs):
        auth_info = validate_token(args[0] if args else None)

        if auth_info:
            kwargs["auth_token"] = auth_info
            return func(*args, **kwargs)
        else:
            return fail_response()
    return wrapper_auth_return