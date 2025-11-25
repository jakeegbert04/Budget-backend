from flask import jsonify, request
from datetime import datetime
from db import db
import functools

from util.validate_uuid import validate_uuid4
from models.auth_tokens import AuthTokens


def validate_token():
    """Validate token from request headers or cookies"""
    auth_token = request.headers.get('auth_token')

    if not auth_token:
        auth_token = request.cookies.get('auth_token')

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
        auth_info = validate_token()  # Just call it directly, no arguments

        if auth_info:
            return func(*args, **kwargs)
        else:
            return fail_response()
    return wrapper_auth_return

def auth_with_return(func):
    @functools.wraps(func)
    def wrapper_auth_return(*args, **kwargs):
        auth_token_record = validate_token()  # Just call it directly, no arguments

        if auth_token_record:
            kwargs["auth_info"] = auth_token_record.user
            return func(*args, **kwargs)
        else:
            return fail_response()
    return wrapper_auth_return