from flask_bcrypt import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from flask import request, jsonify
from sqlalchemy import inspect
from db import db


from util.records import get_record_by_id
from util.reflection import populate_object
from lib.authenticate import auth

class BaseController:
    model = None

    def __init__(self):
        if self.model:
            mapper = inspect(self.model)
            self.primary_key = mapper.primary_key[0]
        
    @auth
    def add(self):
        post_data = request.form or request.json
        record = self.model()  # Just create a new instance directly

        populate_object(record, post_data)

        try:
            db.session.add(record)
            db.session.commit()

        except IntegrityError as e:
            db.session.rollback()
            return jsonify({"message": f"invalid field: {e.orig.diag.constraint_name}"}), 400
        
        return jsonify({"message": "record added", "results": self.model.schema.dump(record)}), 201
    @auth
    def get_all(self):
        records = db.session.query(self.model).all()

        if not records:
            return jsonify({"message": "No records found", "results": []}), 200

        return jsonify({"message": "records found", "results": self.model.schema.dump(records, many=True)}), 200

    @auth
    def get_by_id(self, record_id):
        record = get_record_by_id(self.model, self.primary_key, record_id)

        return jsonify({"message": "record found", "results" : self.model.schema.dump(record)}), 200

    @auth
    def update_by_id(self, record_id):
        post_data = request.form or request.json
        record = get_record_by_id(self.model, self.primary_key, record_id)

        if "password" in post_data and hasattr(record, "password"):
            if check_password_hash(record.password, post_data["password"]):
                return jsonify({"message": "duplicate password", "results": "duplicate password"}), 409

            post_data["password"] = generate_password_hash(post_data["password"]).decode("utf-8")

        populate_object(record, post_data)

        db.session.commit()

        return jsonify({"message": "record updated", "results": self.model.schema.dump(record)}), 200
    @auth
    def delete_by_id(self, record_id):
        record = get_record_by_id(self.model, self.primary_key, record_id)

        db.session.delete(record)
        db.session.commit()

        return jsonify({"message": "record deleted"})
    
    @auth
    def activity(self, record_id):
        record = get_record_by_id(self.model, self.primary_key, record_id)

        record.active = not record.active
        db.session.commit()

        return jsonify({"message": f"record {'activated' if record.active else 'deactivated'}"})