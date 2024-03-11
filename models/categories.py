import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db

class Categories(db.Model):
    __tablename__ = "Categories"

    category_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    amount = db.Column(db.String(), nullable=False )
    category_name = db.Column(db.String(), nullable=False)
    color = db.Column(db.String())
    start_date = db.Column(db.String(), nullable=False)
    end_date = db.Column(db.String())

    def __init__(self, amount, category_name, color, start_date, end_date):
        self.amount = amount
        self.category_name = category_name
        self.color= color
        self.start_date = start_date
        self.end_date = end_date

    def new_user():
        return Categories( "", "", "", "", "")

class CatergoriesSchema(ma.Schema):
    class Meta:
        fields = ['catergory_id', 'amount', 'category_name', 'color', 'start_date', 'end_date']

user_schema = CatergoriesSchema()
users_schema = CatergoriesSchema(many=True)