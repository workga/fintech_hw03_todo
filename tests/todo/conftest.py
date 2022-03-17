import pytest

from app.db import get_db, init_db
from app.todo import manager


@pytest.fixture()
def filled_db(app):
    init_db()

    manager.add_task('A')
    manager.add_task('B')
    manager.add_task('C')
    manager.add_task('D')
    manager.finish_task(3)
    manager.finish_task(4)

    yield get_db()
    init_db()
