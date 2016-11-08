import os

import flask_rdf as flask_rdf
from flask import Flask
from rdflib import Graph
from .hyperflask import Hyperflask
from flask_sqlalchemy import SQLAlchemy


app = Flask('test')
hf = Hyperflask(app)
db = SQLAlchemy(app)


@hf.get('/people')
def people(request_data=None):
    pass


@hf.get('/')
def index(request_data=None):
    return hf.Response(links=people)
