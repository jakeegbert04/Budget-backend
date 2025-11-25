import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone

from models.users import UsersSchema
from models.accounts import AccountsSchema
from models.categories import CategoriesSchema
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
    start_date = db.Column(db.Date(), nullable=False, default=lambda: datetime.now(timezone.utc).date())
    end_date = db.Column(db.DateTime, nullable=True)
    frequency = db.Column(db.String())
    indefinitely = db.Column(db.Boolean(), default=False)
    active = db.Column(db.Boolean(), default=True)

    category = db.relationship('Categories', back_populates='transaction')
    account = db.relationship('Accounts', back_populates='transactions')

class TransactionSchema(ma.Schema):
    class Meta:
        fields = ['transaction_id', "user_id", 'category', 'account', 'amount', "description", "date", "start_date", "end_date", "frequency", "indefinitely", "active"]

    user = ma.fields.Nested(UsersSchema, exclude=("transaction",))
    account = ma.fields.Nested(AccountsSchema)
    category = ma.fields.Nested(CategoriesSchema, exclude=("transaction",))

Transactions.schema = TransactionSchema()