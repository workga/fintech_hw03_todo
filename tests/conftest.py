import pytest

from app import create_app
from app.db import get_db, init_db


@pytest.fixture(autouse=True)
def app():
    app_instance = create_app()
    app_instance.config.update(
        {
            'TESTING': True,
        }
    )
    return app_instance


@pytest.fixture(autouse=True)
def db():
    init_db()
    yield get_db()
    init_db()
