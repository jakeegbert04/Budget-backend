from flask_bcrypt import generate_password_hash
from sqlalchemy.exc import IntegrityError
from flask import jsonify, request
from db import db

from controllers.base_controller import BaseController
from controllers.auth_controller import delete_user_token
from lib.authenticate import auth_with_return
from util.reflection import populate_object
from models.users import Users

class UsersController(BaseController):
    model = Users

    def add(self):
        post_data = request.form or request.json
        record = self.model()

        populate_object(record, post_data)
        
        if hasattr(record, 'password') and record.password:
            record.password = generate_password_hash(record.password).decode("utf8")

        try:
            db.session.add(record)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            return jsonify({"message": f"invalid field: {e.orig.diag.constraint_name}"}), 400
        
        return jsonify({"message": "user created", "results": self.model.schema.dump(record)}), 201

    def update_by_id(self, record_id):
        post_data = request.form or request.json
        existing_record = db.session.query(self.model).filter(
            self.primary_key == record_id
        ).first()
        
        if not existing_record:
            return jsonify({"message": "user not found"}), 404

        populate_object(existing_record, post_data)
        
        # Hash password if it's being updated
        if 'password' in post_data:
            existing_record.password = generate_password_hash(existing_record.password).decode("utf8")
        
        db.session.commit()
        
        return jsonify({"message": "user updated", "results": self.model.schema.dump(existing_record)}), 200
    
    @auth_with_return
    def delete_by_id(self, record_id, auth_info):
        user = db.session.query(self.model).filter(
            self.primary_key == record_id
        ).first()

        if not user:
            return jsonify({"message": "that user doesn't exist"}), 404

        if record_id == auth_info.user_id:
            return jsonify({"message": "can't delete yourself"}), 403

        delete_user_token(record_id)
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({"message": "user deleted"}), 200
    