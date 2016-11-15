from functools import wraps

import json
from flask import url_for, request
from flask_rdf import flask_rdf
from rdflib import Graph


class Hyperflask(object):
    def __init__(self, flask_app, server_state=None):
        self.app = flask_app
        self.server_state = server_state or Graph()

    def resource(self, path, **options):
        def decorator(handler):
            @self.app.route(path, **options)
            @flask_rdf
            @wraps(handler)
            def wrapper(*args, **kwargs):
                return handler(*args, **kwargs)
            return wrapper
        return decorator

    def get(self, path, params=None, **options):
        options.update({'methods': ['GET']})
        return self.resource(path, **options)


def Response(forms=None):
    g = Graph()
    if forms:
        for rel, handler, params in forms:
            href = url_for(handler.__name__)
            g.parse(format='json-ld', data=json.dumps({
                "@context": {
                    "@vocab": "#",
                    "hydra": "http://www.w3.org/ns/hydra/core#",
                },
                '@id': request.path,
                rel: {
                    "@type": "hydra:IriTemplate",
                    "hydra:template": href + "{?" + ','.join(params.keys()) + "}",
                }
            }))
    return g
