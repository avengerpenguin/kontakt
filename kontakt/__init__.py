import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from hyperflask import Hyperflask
from rdflib import Graph

app = Flask("test")
hf = Hyperflask(app)
db = SQLAlchemy(app)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite://")


class Person(db.Model):
    """Example ORM model for a table of person data. The class name
    and field names deliberately following the schema.org
    namespace so we can use a single namespace in the mapping
    from model to RDF graph later."""

    __tablename__ = "people"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(120), unique=True)


@hf.resource("/")
def index():
    return Graph()
