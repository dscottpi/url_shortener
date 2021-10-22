from flask.testing import FlaskClient
from app import __version__
from app import base62, create_app
from app.db import init_db
from app.id_generator import Snowflake

import pytest
import tempfile
import os
import json
import time

@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app({'TESTING': True, 'DATABASE': db_path})

    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client

    os.close(db_fd)
    os.unlink(db_path)

def test_base62_encoder():
    result = base62.encode(11157)
    assert result == '2TX'