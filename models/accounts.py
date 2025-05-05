import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

from models.users import UsersSchema
from db import db

class Accounts(db.Model):
    __tablename__ = "Accounts"

    account_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Users.user_id"), nullable=False)
    account_name = db.Column(db.String(), nullable=False)
    type_of_money = db.Column(db.String())
    balance = db.Column(db.Integer(), nullable=False)
    active = db.Column(db.Boolean())

    transactions = db.relationship('Transactions', back_populates='account')

    def __init__(self, user_id, account_name, type_of_money, balance, active):

        self.user_id = user_id
        self.account_name = account_name
        self.type_of_money = type_of_money
        self.balance= balance
        self.active = active

    def new_account():
        return Accounts( "", "", "", "", True)

class AccountsSchema(ma.Schema):
    class Meta:
        fields = ['account_id', "user_id", 'account_name', 'type_of_money', 'balance', "active"]

    user = ma.fields.Nested(UsersSchema)

account_schema = AccountsSchema()
accounts_schema = AccountsSchema(many=True)