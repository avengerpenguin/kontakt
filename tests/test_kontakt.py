import pytest
import hyperflask
import httpretty
import kontakt


@pytest.fixture
def mock_requests_to_use_flask_test_client():

    client = kontact.app.test_client()

    def get_callback(request, uri, headers):
        r = client.get(uri, headers=headers)
        return (r.status_code, r,headers, r.data)

    httpretty.register_uri(httpretty.GET, '.*', body=request_callback)


def test_index():
    pass
