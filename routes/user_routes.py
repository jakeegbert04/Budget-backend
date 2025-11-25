from flask import Blueprint
from controllers.user_controller import UsersController
from.base_routes import BaseRoutes

user_routes = BaseRoutes("user", UsersController)
user = user_routes.blueprint
