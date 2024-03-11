import functools
from flask import Response
from datetime import datetime

from db import db
from models.auth_tokens import AuthTokens


def validate_token(args):
    auth_token = args.headers.get("authtoken")

    if not auth_token:
        return False

    existing_token = db.session.query(AuthTokens).filter(AuthTokens.auth_token == auth_token).first()

    if existing_token:
        if existing_token.expiration > datetime.now():
            return existing_token
        else:
            return False

def fail_responce():
    return Response("Authentication Required", 401)

def auth_with_return(func):
    @functools.wraps(func)
    def wrapper_auth_return(*args, **kwargs):
        auth_info = validate_token(args[0])

        if auth_info:
            kwargs["auth_info"] = auth_info
            return func(*args, **kwargs)
        else:
            return fail_responce()
    return wrapper_auth_return

def auth(func):
    @functools.wraps(func)
    def wrapper_auth_return(*args, **kwargs):
        auth_info = validate_token(args[0])

        if auth_info:
            return func(*args, **kwargs)
        else:
            return fail_responce()
    return wrapper_auth_return