import json

import os

from flask import Flask, redirect
from flask import Response as HttpResponse
from flask import request
from rdflib import Graph, URIRef
from rdflib import Literal

from .hyperflask import Hyperflask, Response, make_query


app = Flask('test')
app.debug = True
hf = Hyperflask(app)
app.wsgi_app = hf

@hf.query('person-search', '/people/search', {'q': ''})
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


# hf.server_state.parse(format='json-ld', data=json.dumps([
#     {
#         "@id": "/",
#         "#person-search": [
#             {
#                 "@type": [
#                     "http://www.w3.org/ns/hydra/core#IriTemplate"
#                 ],
#                 "http://www.w3.org/ns/hydra/core#template": [
#                     {
#                         "@value": "/people/search{?q}"
#                     }
#                 ]
#             }
#         ]
#     }
# ]))
# print(hf.server_state.serialize(format='turtle'))

@hf.get('/people/<person_id>')
def get_person(person_id):
    r = hf.server_state.query('''
    PREFIX schema: <http://schema.org/>
    CONSTRUCT {
        ?x ?p ?y .
    }
    ''', initBindings={'x': URIRef(request.url)})

    g = Graph()
    for r_ in r:
        g.add(r_)
    return Response(data=g)


@hf.put('/people/<person_id>')
def update_person(person_id):
    g = Graph()
    g.parse(data=request.data.decode('utf-8'), format=request.headers['Content-Type'])
    query = '''INSERT DATA
    {{
        {data}
    }}
    '''.format(data=g.serialize(format='nt').decode('utf-8'))
    print(query)
    r = hf.server_state.update(query)
    return redirect(request.url)


@hf.get('/', links={'person-search': find_person})
def index():
    pass
