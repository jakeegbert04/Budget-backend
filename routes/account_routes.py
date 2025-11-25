from controllers.account_controller import AccountsController
from .base_routes import BaseRoutes

accounts_routes = BaseRoutes("account", AccountsController(), "accounts")
account = accounts_routes.blueprint