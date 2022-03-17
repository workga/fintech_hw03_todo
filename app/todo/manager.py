from app.config import PAGE_SIZE
from app.db import get_db
from app.todo import logger


def page_count(tasks_count: int, page_size: int) -> int:
    if tasks_count == 0:
        return 1

    if tasks_count % page_size == 0:
        return tasks_count // page_size

    return tasks_count // page_size + 1


def find_tasks(
    active_filter: str = 'all',
    text_filter: str = '',
    page: int = 1,
    page_size: int = PAGE_SIZE,
):
    db = get_db()
    tasks = db.execute(
        'SELECT id, text, active FROM task ORDER BY created DESC ',
    ).fetchall()

    if active_filter == 'active':
        tasks = [t for t in tasks if t['active']]
    elif active_filter == 'finished':
        tasks = [t for t in tasks if not t['active']]

    if text_filter:
        tasks = [t for t in tasks if text_filter in t['text']]

    max_page = page_count(len(tasks), page_size)
    page = max(page, 0)
    page = min(page, max_page)
    tasks = tasks[
        min(len(tasks) - 1, (page - 1) * page_size) : min(len(tasks), page * page_size)
    ]
    return tasks, page, max_page


def add_task(task_text: str) -> None:
    if not task_text:
        return

    db = get_db()
    db.execute('INSERT INTO task (text) VALUES (?)', (task_text,))
    db.commit()

    logger.info(f"Added task: '{task_text}'")


def finish_task(task_id: int) -> None:
    if task_id is None or task_id == -1:
        return

    db = get_db()
    db.execute('UPDATE task SET active = FALSE WHERE id = (?)', (task_id,))
    db.commit()

    task = db.execute('SELECT * FROM task WHERE id = (?)', (task_id,)).fetchone()

    if task is None:
        return

    logger.info(f"Finished task: '{task['text']}'")
