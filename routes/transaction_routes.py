from controllers.transaction_controller import TransactionsController
from .base_routes import BaseRoutes


transactions_routes = BaseRoutes("transaction", TransactionsController, "transactions")
transaction = transactions_routes.blueprint