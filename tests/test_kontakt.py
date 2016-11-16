import re
import pytest
import httpretty
import requests
from rdflib import Graph

import kontakt
import hyperspace
from laconia import ThingFactory


@pytest.fixture(autouse=True, scope='module')
def mock_requests_to_use_flask_test_client(request):

    client = kontakt.app.test_client()

    g = Graph()
    g.parse(format='turtle', data='''
    @prefix schema: <http://schema.org/> .
    <http://example.com/people/1> a schema:Person ;
                schema:name "Ross" .
    ''')
    kontakt.hf.server_state = g

    def get_callback(http_request, uri, headers):

        r = client.get(uri, headers=dict(http_request.headers))

        response_headers = {
            'content-type': r.headers['Content-Type'],
            'content-length': len(r.headers['Content-Length']),
        }
        response_headers.update(headers)

        return int(r.status_code), response_headers, r.data

    httpretty.register_uri(httpretty.GET, re.compile('.*'), body=get_callback)
    httpretty.enable()

    request.addfinalizer(httpretty.disable)
    request.addfinalizer(httpretty.reset)


def test_index():
    http = requests.Session()
    http.headers = {'Accept': 'text/turtle'}
    page = hyperspace.jump('http://example.com/', http)
    assert page.response.status_code == 200


def test_search():
    http = requests.Session()
    http.headers = {'Accept': 'text/turtle'}
    page = hyperspace.jump('http://example.com/', http)
    assert len(page.queries) == 1
    results = page.queries['#person-search'][0].build({'q': 'Ross'}).submit()
    assert results.response.status_code == 200


def test_search_results():
    http = requests.Session()
    http.headers = {'Accept': 'text/turtle'}
    page = hyperspace.jump('http://example.com/', http)

    results = page.queries['#person-search'][0].build({'q': 'Ross'}).submit()
    results.data.bind('schema', 'http://schema.org/', override=True)

    Thing = ThingFactory(results.data)
    ross = Thing('http://example.com/people/1')
    assert 'Ross' in ross.schema_name
