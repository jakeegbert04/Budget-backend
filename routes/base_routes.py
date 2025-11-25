from flask import Blueprint

class BaseRoutes:
    def __init__(self, blueprint_name, controller, plural_name=None):
        self.set_route_variables(blueprint_name, controller, plural_name)

        self.add_route(f"/{self.route_name}", methods=["POST"], view_func=self.controller.add)
        self.add_route(f"/{self.plural_name}", methods=["GET"], view_func=self.controller.get_all)
        self.add_route(f"/{self.route_name}/<uuid:record_id>", methods=["GET"], view_func=self.controller.get_by_id)
        self.add_route(f"/{self.route_name}/<uuid:record_id>", methods=["PUT"], view_func=self.controller.update_by_id)
        self.add_route(f"/{self.route_name}/<uuid:record_id>", methods=["PATCH"], view_func=self.controller.activity)
        self.add_route(f"/{self.route_name}/delete/<uuid:record_id>", methods=["DELETE"], view_func=self.controller.delete_by_id)

    def set_route_variables(self, blueprint_name, controller, plural_name=None):
        self.controller = controller() if isinstance(controller, type) else controller
        self.blueprint = Blueprint(blueprint_name, __name__)
        self.url_rules = {}
        self.route_name = blueprint_name
        self.plural_name = plural_name if plural_name else f"{blueprint_name}s"

    def add_route(self, rule, **kwargs):
        """Add a route to the blueprint"""
        view_func = kwargs.pop("view_func")  # Remove from kwargs to avoid duplicate
        
        if not view_func:
            raise ValueError("view_func is required")
        
        # Store the route info for tracking
        self.url_rules[view_func] = (rule, kwargs, view_func)
        
        # Add to blueprint - now view_func is not in kwargs anymore
        self.blueprint.add_url_rule(rule, view_func=view_func, **kwargs)

    def remove_route(self, view_func):
        """Remove a route from tracking"""
        if view_func in self.url_rules:
            del self.url_rules[view_func]
        else:
            raise KeyError(f"Route with view_func {view_func} not found")

    def add_url_rules(self):
        """Re-register all tracked routes"""
        for (rule, kwargs, view_func) in self.url_rules.values():
            self.blueprint.add_url_rule(rule, view_func=view_func, **kwargs)