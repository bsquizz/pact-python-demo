import atexit
import unittest

from pact import Consumer, Like, Provider, Term
import pytest

from .client import UserClient

PACT_MOCK_HOST = 'localhost'
PACT_MOCK_PORT = 1234


@pytest.fixture
def client():
    return UserClient(
        'http://{host}:{port}'
        .format(host=PACT_MOCK_HOST, port=PACT_MOCK_PORT)
    )


@pytest.fixture(scope='module')
def pact():
    pact = Consumer('Consumer').has_pact_with(
        Provider('Provider'), host_name=PACT_MOCK_HOST, port=PACT_MOCK_PORT)
    pact.start_service()
    atexit.register(pact.stop_service)
    return pact


def test_get_user_non_admin(pact, client):
    expected = {
        'name': 'UserA',
        'id': Term(
            r'^[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}\Z',
            '00000000-0000-4000-a000-000000000000'
        ),
        'created_on': Term(
            r'\d+-\d+-\d+T\d+:\d+:\d+',
            '2016-12-15T20:16:01'
        ),
        'admin': False
    }

    (pact
     .given('UserA exists and is not an administrator')
     .upon_receiving('a request for UserA')
     .with_request('get', '/users/UserA')
     .will_respond_with(200, body=Like(expected)))

    with pact:
        result = client.get_user('UserA')

    # assert something with the result, for ex, did I process 'result' properly?
    # or was I able to deserialize correctly? etc.

def test_get_non_existing_user(pact, client):
    (pact
     .given('UserA does not exist')
     .upon_receiving('a request for UserA')
     .with_request('get', '/users/UserA')
     .will_respond_with(404))

    with pact:
        result = client.get_user('UserA')

    assert result is None
