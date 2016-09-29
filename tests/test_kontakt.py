import re
import pytest
import hyperflask
import httpretty
import kontakt
import hyperspace


@pytest.fixture(autouse=True, scope='module')
def mock_requests_to_use_flask_test_client(request):

    client = kontakt.app.test_client()

    def get_callback(http_request, uri, headers):
        print(dict(http_request.headers))
        r = client.get(uri, headers=dict(http_request.headers))

        response_headers = {
            'content-type': r.headers['Content-Type'],
            'content-length': len(r.headers['Content-Length']),
        }
        response_headers.update(headers)

        print(dict(r.headers))
        return int(r.status_code), response_headers, r.data

    httpretty.register_uri(httpretty.GET, re.compile('.*'), body=get_callback)
    httpretty.enable()

    request.addfinalizer(httpretty.disable)
    request.addfinalizer(httpretty.reset)


def test_index():
    page = hyperspace.jump('http://example.com/')
    assert page.response.status_code == 200
