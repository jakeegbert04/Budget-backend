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

def validate_token(req=None):
    if not req:
        req = request

    auth_token = req.headers.get('auth_token')

    if not auth_token:
        auth_token = req.cookies.get('auth_token')

    if not auth_token or not validate_uuid4(auth_token):
        return False

    token_record = db.session.query(AuthTokens).filter(
        AuthTokens.auth_token == auth_token,
        AuthTokens.expiration > datetime.now()
    ).first()

    return token_record if token_record else False

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
        auth_token_record = validate_token(args[0] if args else None)

        if auth_token_record:
            kwargs["auth_info"] = auth_token_record.user  # <-- Return the user, not the token
            return func(*args, **kwargs)
        else:
            return fail_response()
    return wrapper_auth_return