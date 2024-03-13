# CREATE
from flask import request, jsonify
from flask_bcrypt import generate_password_hash

from db import db
from models.users import user_schema, users_schema, Users
from controllers.auth_controller import delete_user_token
from util.reflection import populate_object
from lib.authenticate import auth

# @auth
def add_user(request):
    req_data = request.form if request.form else request.get_json()

    if not req_data:
        return jsonify({"message" : "please enter all required fields"}), 400

    new_user = Users.new_user()

    populate_object(new_user, req_data)
    new_user.password = generate_password_hash(new_user.password).decode("utf8")

    try:
        db.session.add(new_user)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to create record"}), 400

    return jsonify({"message": "user created", "results": user_schema.dump(new_user)}), 201

@auth
def get_all_active_users(request):
    users = db.session.query(Users).filter(Users.active == True).all()

    if not users:
        return jsonify({"message" : "no active users exist"}), 404
    else:
        return jsonify({"message" : "fetched users", "results" : users_schema.dump(users)}), 200

@auth
def get_users_by_id(request, id):
    user = db.session.query(Users).filter(Users.user_id == id).first()

    if not user:
        return jsonify({"message" : "that user doesn't exist"}), 404

    else:
        return jsonify(user_schema.dump(user)), 200

@auth
def update_user(request, id):
    req_data = request.form if request.form else request.json
    existing_user = db.session.query(Users).filter(Users.user_id == id).first()

    populate_object(existing_user, req_data)

    existing_user.password = generate_password_hash(existing_user.password).decode("utf8")

    db.session.commit()

    return jsonify({"message": "user updated", "results" : user_schema.dump(existing_user)}), 201

@auth
def user_status(request, id):
    user_data = db.session.query(Users).filter(Users.user_id == id).first()

    if user_data:
        user_data.active = not user_data.active
        db.session.commit()

        return jsonify(user_schema.dump(user_data)), 200
    return jsonify({"message": "no user found"}), 404

@auth
def delete_user(request, id, auth_info):

    user = db.session.query(Users).filter(Users.user_id == id).first()

    if not user:
        return jsonify({"message" : "that user doesn't exist"}), 404

    if id == str(auth_info.user_id):
        return jsonify({"message" : "can't delete yourself"}), 404

    delete_user_token(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message" : "user deleted"})