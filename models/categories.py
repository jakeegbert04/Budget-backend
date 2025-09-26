import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

from db import db

class Categories(db.Model):
    __tablename__ = 'Categories'

    category_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Users.user_id'), nullable=False)
    amount = db.Column(db.String(), nullable=False )
    name = db.Column(db.String(), nullable=False)
    color = db.Column(db.String())
    start_date = db.Column(db.String(), nullable=False, default=lambda: datetime.today().strftime('%Y-%m-%d'))
    end_date = db.Column(db.String())
    active = db.Column(db.Boolean())

    transaction = db.relationship('Transactions', back_populates='category')

    def __init__(self, user_id, amount, name, color, start_date, end_date, active):
        self.user_id = user_id
        self.amount = amount
        self.name = name
        self.color= color
        self.start_date = start_date
        self.end_date = end_date
        self.active = active

    def new_category():
        return Categories( '', '', '', '', '', '', True)

class CategoriesSchema(ma.Schema):
    class Meta:
        fields = ['category_id', 'user_id', 'amount', 'name', 'color', 'start_date', 'end_date', 'transaction', 'active']
        
    transaction = ma.fields.Nested('TransactionSchema', many=True, exclude=('category',))
        
category_schema = CategoriesSchema()
categories_schema = CategoriesSchema(many=True)