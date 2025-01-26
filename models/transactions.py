import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID

from models.users import UsersSchema
from db import db

class Transactions(db.Model):
    __tablename__ = "Transactions"

    transaction_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Users.user_id"), nullable=False)
    category_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Categories.category_id"), nullable=False)
    account_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Accounts.account_id"), nullable=False)
    amount = db.Column(db.String(), nullable=False)
    description = db.Column(db.String())
    date = db.Column(db.DateTime, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    frequency = db.Column(db.String())
    active = db.Column(db.Boolean())

    category = db.relationship('Categories', back_populates='transaction')

    def __init__(self, user_id, category_id, account_id, amount, description, date, start_date, end_date, frequency, active ):

        self.user_id = user_id
        self.category_id = category_id
        self.account_id = account_id
        self.amount = amount
        self.description = description
        self.date = date
        self.start_date = start_date
        self.end_date = end_date
        self.frequency = frequency
        self.active = active

    def new_transaction():
        return Transactions( "", "", "", "", "", "", "", "", "", True)

class TransactionSchema(ma.Schema):
    class Meta:
        fields = ['transaction_id', "user_id", 'category', 'account_id', 'amount', "description", "date", "start_date", "end_date", "frequency", "active"]

    user = ma.fields.Nested(UsersSchema, exclude=("transaction",))

transaction_schema = TransactionSchema()
transactions_schema = TransactionSchema(many=True)