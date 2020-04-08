import os
import tempfile

import pytest

from blog import index


@pytest.fixture
def client():
    db_fd, index.app.config['DATABASE'] = tempfile.mkstemp()
    index.app.config['TESTING'] = True
    index.app.config['PASSWORD'] = 'testPassword123'

    with index.app.test_client() as client:
        yield client

    os.close(db_fd)
    os.unlink(index.app.config['DATABASE'])


def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)

    
def test_empty_db(client):
    """Start with a blank database."""

    rv = client.get('/')
    assert b'No hay posteos todavía.' in rv.data


def test_login_logout(client):
    """Make sure login and logout works."""

    rv = login(client, 'USERNAME', index.app.config['PASSWORD'])
    assert b'You are now logged in.' in rv.data

    rv = logout(client)
    assert b'You were logged out' in rv.data

    rv = login(client, 'USERNAME', index.app.config['PASSWORD'] + 'x')
    assert b'Incorrect password' in rv.data

