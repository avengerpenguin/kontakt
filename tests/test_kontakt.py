import pytest
import hyperflask
import httpretty
import kontakt
import hyperspace


@pytest.fixture(autouse=True)
def mock_requests_to_use_flask_test_client():

    client = kontakt.app.test_client()

    def get_callback(request, uri, headers):
        r = client.get(uri, headers=headers)
        return (r.status_code, r,headers, r.data)

    httpretty.register_uri(httpretty.GET, '.*', body=get_callback)


def test_index():
    page = hyperspace.jump('http://example.com/')
    assert page.response.status_code == 200
