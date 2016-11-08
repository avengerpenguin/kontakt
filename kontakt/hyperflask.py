from functools import wraps

import flask_rdf as flask_rdf
from rdflib import Graph


class Hyperflask(object):
    def __init__(self, flask_app, server_state=None):
        self.app = flask_app
        self.server_state = server_state or Graph()

    def resource(self, path):
        def decorator(handler):
            @self.app.route(path)
            @flask_rdf
            @wraps(handler)
            def wrapper(*args, **kwargs):
                return handler(*args, **kwargs)
            return wrapper
        return decorator
