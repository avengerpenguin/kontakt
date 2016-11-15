import os

from flask import Flask
from flask import request

from .hyperflask import Hyperflask, Response


app = Flask('test')
hf = Hyperflask(app)


@hf.get('/people/search')
def find_person():
    q = request.args.get('q')
    r = hf.server_state.query('''
    PREFIX schema: <http://schema.org/>
    CONSTRUCT {
        ?x a schema:Person .
        ?x ?p ?y .
    }
    WHERE {
        ?x schema:name ?name
    }
    ''', initBindings={'name': q})
    print(r)
    return Response()


@hf.get('/')
def index():
    return Response(forms=[
        ('person-search', find_person, {'q': ''}),
    ])
