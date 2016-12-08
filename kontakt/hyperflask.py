from functools import wraps

import json
from flask import url_for, request
from flask_rdf import flask_rdf
from rdflib import Graph, URIRef, BNode, RDF, Namespace


HYDRA = Namespace('http://www.w3.org/ns/hydra/core#')


class Hyperflask(object):
    def __init__(self, flask_app, server_state=None):
        self.app = flask_app
        self.server_state = server_state or Graph()
        self.links = []

        self.app.add_url_rule('/', view_func=self.fallback_get, methods=['GET'])

    def resource(self, path, links=None, **options):
        if links:
            for rel, handler in links.items():
                self.links.append((path, rel, handler))
                #href = url_for(handler.__name__)
                #self.server_state.add((URIRef(path), URIRef(rel), href))

        def decorator(handler):
            @self.app.route(path, **options)
            @flask_rdf
            @wraps(handler)
            def wrapper(*args, **kwargs):
                graph = handler(*args, **kwargs)
                if graph:
                    return graph
                else:
                    self.fallback_get()

            return wrapper

        return decorator

    def get(self, path, **options):
        options.update({'methods': ['GET']})
        return self.resource(path, **options)

    def put(self, path, **options):
        options.update({'methods': ['PUT']})
        return self.resource(path, **options)

    @flask_rdf
    def fallback_get(self, path=None):
        print(self.server_state.serialize(format='turtle'))
        r = self.server_state.query('''
        PREFIX schema: <http://schema.org/>
        CONSTRUCT
        WHERE {
            ?x ?p ?y .
        }
        ''', initBindings={'x': URIRef(request.url)})

        g = Graph()
        for r_ in r:
            g.add(r_)
        return Response(data=g)

    def query(self, name, path, params):
        b = BNode()
        self.server_state.add((b, RDF.type, HYDRA.IriTemplate))
        self.server_state.add(
                (b,
                 HYDRA.template,
                 URIRef(path + "{?" + ','.join(params.keys()) + "}")))
        return self.get(path)

    def __call__(self, environ, start_response):
        for path, rel, handler in self.links:
            href = url_for(handler.__name__)
            self.server_state.add((URIRef(path), URIRef(rel), href))
        self.app(environ, start_response)


def Response(forms=None, data=None, links=None):
    g = data or Graph()
    if forms:
        for rel, handler, params in forms:
            href = url_for(handler.__name__)
            g.parse(format='json-ld', data=json.dumps({
                "@context": {
                    "@vocab": request.url + "#",
                    "hydra": "http://www.w3.org/ns/hydra/core#",
                },
                '@id': request.url,
                rel: {
                    "@type": "hydra:IriTemplate",
                    "hydra:template": href + "{?" + ','.join(
                        params.keys()) + "}",
                }
            }))

    print(g.serialize(format='json-ld'))
    return g


def make_query(handler, href, params):
    return {
        "@type": "http://www.w3.org/ns/hydra/core#IriTemplate",
        "http://www.w3.org/ns/hydra/core#template": href + "{?" + ','.join(params.keys()) + "}",
    }
