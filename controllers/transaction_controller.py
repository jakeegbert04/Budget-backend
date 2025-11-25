from .base_controller import BaseController
from models.transactions import Transactions

class TransactionsController(BaseController):
    model = Transactions