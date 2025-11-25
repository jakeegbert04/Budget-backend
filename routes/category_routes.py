from controllers.category_controller import CategoriesController
from .base_routes import BaseRoutes

categories_routes = BaseRoutes("category", CategoriesController(), "categories")

category = categories_routes.blueprint