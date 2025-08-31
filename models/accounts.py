import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

from models.users import UsersSchema
from db import db

class Accounts(db.Model):
    __tablename__ = 'Accounts'

    account_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Users.user_id'), nullable=False)
    name = db.Column(db.String(), nullable=False)
    account_type = db.Column( db.Enum('cash', 'credit', 'debit', 'savings', name='account_type_enum'), nullable=False)
    balance = db.Column(db.Integer(), nullable=False)
    active = db.Column(db.Boolean())

    transactions = db.relationship('Transactions', back_populates='account')

    def __init__(self, user_id, name, account_type, balance, active):

        self.user_id = user_id
        self.name = name
        self.account_type = account_type
        self.balance= balance
        self.active = active

    def new_account():
        return Accounts( '', '', '', '', True)

class AccountsSchema(ma.Schema):
    class Meta:
        fields = ['account_id', 'user_id', 'name', 'account_type', 'balance', 'active']

    user = ma.fields.Nested(UsersSchema)

account_schema = AccountsSchema()
accounts_schema = AccountsSchema(many=True)