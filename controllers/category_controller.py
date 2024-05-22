from flask import request, jsonify
from flask_bcrypt import generate_password_hash

from db import db
from models.categories import category_schema, categories_schema, Categories
from util.reflection import populate_object
from lib.authenticate import auth

@auth
def add_category(request):
    req_data = request.form if request.form else request.get_json()

    if not req_data:
        return jsonify({"message" : "please enter all required fields"}), 400
    
    new_category = Categories.new_category()

    populate_object(new_category, req_data)
    
    try:
        db.session.add(new_category)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message":"unable to create record"}), 400
    
    return jsonify({"message": "category created", "results":category_schema.dump(new_category)}), 201
@auth
def update_category(request, id):
    req_data = request.form if request.form else request.json
    existing_category = db.session.query(Categories).filter(Categories.category_id == id).first()

    if not existing_category:
        return jsonify({"message":"no existing category"})
    
    populate_object(existing_category, req_data)

    return jsonify({"message":"user updated", "results": category_schema.dump(existing_category)}), 201

@auth
def get_all_active_categories(request):
    categories = db.session.query(Categories).all()

    if not categories:
        return jsonify({"message": "no categories exist"}), 404
    else:
        return jsonify({"message": "fetched categories", "results": categories_schema.dump(categories)}), 200

@auth
def get_category_by_id(request, id):
    category = db.session.query(Categories).filter(Categories.category_id == id).first()

    if not category:
        return jsonify({"message": "category doesn't exist"}),404
    else:
        return jsonify({"message":"fetched category", "results": category_schema.dump(category)}), 200

@auth
def category_status(request, id):
    category_data = db.session.query(Categories).filter(Categories.category_id == id).first()

    if category_data:
        category_data.active = not category_data.active
        db.session.commit()

        return jsonify({"message":"changed status of category", "results": category_schema.dump(category_data)}), 200
    return jsonify({"message":"no category found"}), 404

@auth
def delete_category(request, id):
    category = db.session.query(Categories).filter(Categories.category_id == id).first()

    if not category:
        return jsonify({"message":"catgegory doesn't exist"}), 404
    
    db.session.delete(category)
    db.session.commit()
    return jsonify({"message": "category deleted"}), 200