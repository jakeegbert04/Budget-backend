from controllers.roles_contoller import RolesController
from .base_routes import BaseRoutes

roles_routes = BaseRoutes("roles", RolesController)
role = roles_routes.blueprint