import pytest
from flask import url_for


@pytest.mark.parametrize(
    ('active_filter', 'text_filter', 'page'),
    [
        ('all', '', 1),
        ('active', '', 1),
        ('finished', '', 1),
        ('all', 'A', 1),
        ('all', '', 2),
        (None, None, None),
        (None, None, 100),
        (None, None, 0),
    ],
)
def test_tasks_get(app, filled_db, active_filter, text_filter, page):
    args = {
        'active_filter': active_filter,
        'text_filter': text_filter,
        'page': page,
    }

    with app.test_client() as client:
        response = client.get(url_for('tasks', **args))

    assert len(response.history) == 0
    assert response.request.path == '/tasks'
    assert response.status_code == 200


@pytest.mark.parametrize(
    ('task_text'),
    [
        ('some task'),
        (''),
        (None),
    ],
)
def test_tasks_post(mocker, app, db, task_text):
    mocked_add_task = mocker.patch('app.todo.manager.add_task')

    with app.test_client() as client:
        response = client.post(
            '/tasks',
            follow_redirects=True,
            headers={'Referer': '/tasks'},
            data={'task_text': task_text},
        )

    assert len(response.history) == 1
    assert response.history[0].status_code == 302

    assert response.request.path == '/tasks'
    assert response.status_code == 200

    mocked_add_task.assert_called_with(task_text)


@pytest.mark.parametrize(
    ('task_id'),
    [
        (1),
        (None),
    ],
)
def test_tasks_finish_post(mocker, app, filled_db, task_id):
    mocked_finish_task = mocker.patch('app.todo.manager.finish_task')

    with app.test_client() as client:
        response = client.post(
            '/tasks/finish',
            follow_redirects=True,
            headers={'Referer': '/tasks'},
            data={'task_id': task_id},
        )

    assert len(response.history) == 1
    assert response.history[0].status_code == 302

    assert response.request.path == '/tasks'
    assert response.status_code == 200

    mocked_finish_task.assert_called_with(task_id)
