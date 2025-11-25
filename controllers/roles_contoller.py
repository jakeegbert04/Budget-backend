from controllers.base_controller import BaseController
from models.roles import Roles
from flask import jsonify
from db import db

class RolesController(BaseController):
    model = Roles

    def update_by_id(self, record_id):
        record = db.session.query(self.model).filter(
            self.primary_key == record_id
        ).first()
        
        if not record:
            return jsonify({"message": "role not found"}), 404
            
        if record.name == "super_admin":
            return jsonify({"message": "cannot update super admin"}), 403
        
        return super().update_by_id(record_id)
    
    def activity(self, record_id):
        record = db.session.query(self.model).filter(
            self.primary_key == record_id
        ).first()
        
        if not record:
            return jsonify({"message": "role not found"}), 404
            
        if record.name == "super_admin":
            return jsonify({"message": "cannot deactivate a super admin"}), 403
        
        return super().activity(record_id)
    
    def delete_by_id(self, record_id):
        record = db.session.query(self.model).filter(
            self.primary_key == record_id
        ).first()
        
        if not record:
            return jsonify({"message": "role not found"}), 404
            
        if record.name == "super_admin":
            return jsonify({"message": "cannot delete a super admin"}), 403
        
        return super().delete_by_id(record_id)