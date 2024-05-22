from flask import Blueprint, request
from controllers import category_controller

category = Blueprint("category", __name__)

@category.route('/category/add', methods=["POST"])
def add_category():
    return category_controller.add_category(request)

@category.route('/category/update/<id>', methods=["PUT"])
def update_category(id):
    return category_controller.update_category(request, id)

@category.route('/categories', methods=['GET'])
def get_all_active_categories():
    return category_controller.get_all_active_categories(request)

@category.route("/category/<id>", methods=["GET"])
def get_category_by_id(id):
    return category_controller.get_category_by_id(request, id)

@category.route("/category/<id>", methods=["PATCH"])
def category_status(id):
    return category_controller.category_status(request, id)

@category.route('/category/delete/<id>', methods=["DELETE"])
def delete_category(id):
    return category_controller.delete_category(request, id)