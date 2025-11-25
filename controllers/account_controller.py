from .base_controller import BaseController
from models.accounts import Accounts

class AccountsController(BaseController):
    model = Accounts