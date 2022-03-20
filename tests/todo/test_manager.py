import pytest

from app.todo import manager
from tests.todo.conftest import fill_db


@pytest.mark.parametrize(
    ('tasks_count', 'page_size', 'result'),
    [
        (0, 10, 1),
        (1, 10, 1),
        (9, 10, 1),
        (10, 10, 1),
        (11, 10, 2),
        (19, 10, 2),
        (20, 10, 2),
        (21, 10, 3),
    ],
)
def test_page_count(tasks_count, page_size, result):
    assert manager.page_count(tasks_count, page_size) == result


@pytest.mark.parametrize(
    'text',
    [
        'some task',
    ],
)
def test_add_task_success(db, text):
    manager.add_task(text)

    count = db.execute(
        'SELECT COUNT(*) as count FROM task WHERE text = (?)', (text,)
    ).fetchone()['count']
    assert count == 1


@pytest.mark.parametrize(
    'text',
    [
        '',
        None,
    ],
)
def test_add_task_fail(db, text):
    manager.add_task(text)

    count = db.execute(
        'SELECT COUNT(*) as count FROM task WHERE text = (?)', (text,)
    ).fetchone()['count']
    assert count == 0


@pytest.mark.parametrize(
    ('task_id', 'task_text'),
    [
        (1, 'some text'),
    ],
)
def test_finish_task_success(db, task_id, task_text):
    manager.add_task(task_text)

    active = db.execute(
        'SELECT active FROM task WHERE id = (?)', (task_id,)
    ).fetchone()['active']
    assert active

    manager.finish_task(task_id)

    active = db.execute(
        'SELECT active FROM task WHERE id = (?)', (task_id,)
    ).fetchone()['active']
    assert not active


@pytest.mark.parametrize(
    ('task_id', 'task_text'),
    [
        (2, 'some text'),
        (-1, 'some text'),
        (None, 'some text'),
    ],
)
def test_finish_task_fail(db, task_id, task_text):
    manager.add_task(task_text)

    active = db.execute(
        'SELECT active FROM task WHERE text = (?)', (task_text,)
    ).fetchone()['active']
    assert active

    manager.finish_task(task_id)

    active = db.execute(
        'SELECT active FROM task WHERE text = (?)', (task_text,)
    ).fetchone()['active']
    assert active


@pytest.mark.parametrize(
    ('active_filter', 'text_filter', 'page', 'page_size', 'count'),
    [
        ('all', '', 1, 2, 2),
        ('active', '', 1, 2, 2),
        ('finished', '', 1, 2, 2),
        ('all', 'A', 1, 2, 1),
        ('all', '', 2, 3, 1),
        ('all', '', 3, 2, 2),
        ('active', '', 2, 1, 1),
        ('active', 'D', 1, 2, 0),
    ],
)
def test_find_tasks(active_filter, text_filter, page, page_size, count):
    fill_db()
    tasks, _, _ = manager.find_tasks(
        active_filter=active_filter,
        text_filter=text_filter,
        page=page,
        page_size=page_size,
    )

    assert len(tasks) == count
