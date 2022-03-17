import pytest

from app import create_app
from app.db import get_db, init_db


@pytest.fixture
def app():
    app = create_app()
    app.config.update(
        {
            'TESTING': True,
        }
    )
    return app


@pytest.fixture()
def db(app):
    init_db()
    yield get_db()
    init_db()
