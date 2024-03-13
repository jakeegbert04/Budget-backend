from flask import request, jsonify
from flask_bcrypt import generate_password_hash

from db import db
from models.categories import category_schema, categories_schema, Categories
from util.reflection import populate_object
from lib.authenticate import auth, auth_with_return

# @auth
# def add_category(request):
    