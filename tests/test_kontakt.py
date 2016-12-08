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

    def put_callback(http_request, uri, headers):

        r = client.put(uri, data=http_request.body, headers=dict(http_request.headers))

        response_headers = {
            'content-type': r.headers['Content-Type'],
            'content-length': len(r.headers['Content-Length']),
        }
        response_headers.update(headers)

        return int(r.status_code), response_headers, r.data

    httpretty.register_uri(httpretty.GET, re.compile('.*'), body=get_callback)
    httpretty.register_uri(httpretty.PUT, re.compile('.*'), body=put_callback)
    httpretty.enable()

    request.addfinalizer(httpretty.disable)
    request.addfinalizer(httpretty.reset)


@pytest.fixture
def entrypoint():
    http = requests.Session()
    http.headers = {'Accept': 'text/turtle'}
    return hyperspace.jump('http://example.com/', http)


def test_index(entrypoint):
    assert entrypoint.response.status_code == 200


def test_search(entrypoint):
    results = entrypoint.queries['#person-search'][0].build({'q': 'Ross'}).submit()
    assert results.response.status_code == 200


def test_search_results(entrypoint):
    results = entrypoint.queries['#person-search'][0].build({'q': 'Ross'}).submit()
    ross = results.entity('http://example.com/people/1')
    assert 'Ross' in ross.schema_name


def test_search_results(entrypoint):
    page = entrypoint.queries['#person-search'][0].build({'q': 'Ross'}).submit()
    ross = page.entity('http://example.com/people/1')
    assert 'ross@example.com' not in ross.schema_email
    ross.schema_email.add('ross@example.com')
    ross.update()

    page = entrypoint.queries['#person-search'][0].build({'q': 'Ross'}).submit()
    ross = page.entity('http://example.com/people/1')
    assert 'ross@example.com' in ross.schema_email
