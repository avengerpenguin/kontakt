import os

from flask import Flask
from flask import request
from rdflib import Graph
from rdflib import Literal

from .hyperflask import Hyperflask, Response


app = Flask('test')
hf = Hyperflask(app)


@hf.get('/people/search')
def find_person():
    q = request.args.get('q')

    r = hf.server_state.query('''
    PREFIX schema: <http://schema.org/>
    CONSTRUCT {
        ?x ?p ?y .
    }
    WHERE {
        ?x a schema:Person .
        ?x ?p ?y .
        ?x schema:name ?name .
    }
    ''', initBindings={'name': Literal(q)})

    g = Graph()
    for r_ in r:
        g.add(r_)
    return Response(data=g)


@hf.get('/')
def index():
    return Response(forms=[
        ('person-search', find_person, {'q': ''}),
    ])
