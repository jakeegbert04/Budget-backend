from flask import abort, make_response
from db import db

from util.validate_uuid import validate_uuid4

def get_record_by_id(model, key, record_id):
            if not validate_uuid4(record_id):
               abort(make_response({"message": "record not found"}))

            record = db.session.query(model).filter(key == record_id).first()

            if not record:
                abort(make_response({"message": "record not found"}, 404))

            return record