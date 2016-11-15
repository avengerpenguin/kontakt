#!/usr/bin/env python

from setuptools import setup

setup(
    name="kontakt",
    version="0.0.0",
    author='Ross Fenning',
    author_email='Ross.Fenning@gmail.com',
    packages=['kontakt'],
    description='Website and API for contact data',
    url='http://github.com/avengerpenguin/kontakt',
    install_requires=['flask', 'flask-sqlalchemy', 'flask_rdf', 'rdflib', 'hyperspace'],
    setup_requires=['pytest-runner',],
    tests_require=['pytest', 'httpretty'],
)
