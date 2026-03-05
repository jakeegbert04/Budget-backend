from flask import request, jsonify
from sqlalchemy.exc import IntegrityError
from decimal import Decimal

from models.categories import Categories
from .base_controller import BaseController
from models.transactions import Transactions
from util.reflection import populate_object
from lib.authenticate import auth
from db import db

class TransactionsController(BaseController):
    model = Transactions

    def _save_transaction(self, record):
        """Shared logic for saving a transaction and updating category balance."""
        category = Categories.query.get(record.category_id)
        if not category:
            return False, "category not found"

        current = Decimal(category.amount)
        txn_amount = Decimal(record.amount)
        category.amount = str(current + txn_amount)

        db.session.add(record)
        return True, None

    @auth
    def add(self):
        post_data = request.form or request.json
        record = Transactions()
        populate_object(record, post_data)

        try:
            success, error = self._save_transaction(record)
            if not success:
                return jsonify({"message": error}), 404
            db.session.commit()

        except IntegrityError as e:
            db.session.rollback()
            return jsonify({"message": f"invalid field: {e.orig.diag.constraint_name}"}), 400

        return jsonify({"message": "record added", "results": self.model.schema.dump(record)}), 201