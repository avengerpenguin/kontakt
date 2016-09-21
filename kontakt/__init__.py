import os
from flask import Flask
from rdflib import Graph
from hyperflask import Hyperflask
from flask_sqlalchemy import SQLAlchemy


app = Flask('test')
hf = Hyperflask(app)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite://')


@hf.resource('/')
def index():
    return Graph()
