from app.config import PAGE_SIZE
from app.db import get_db
from app.todo import logger


def page_count(tasks_count: int) -> int:
    if tasks_count == 0:
        return 1

    if tasks_count % PAGE_SIZE == 0:
        return tasks_count // PAGE_SIZE

    return tasks_count // PAGE_SIZE + 1


def find_tasks(active_filter: str, text_filter: str, page: int):
    db = get_db()
    tasks = db.execute(
        'SELECT * FROM task ' 'ORDER BY created DESC ',
    ).fetchall()

    if active_filter == 'active':
        tasks = [t for t in tasks if t['active']]
    elif active_filter == 'finished':
        tasks = [t for t in tasks if not t['active']]

    if text_filter:
        tasks = [t for t in tasks if text_filter in t['text']]

    max_page = page_count(len(tasks))
    page = min(page, max_page)
    tasks = tasks[
        min(len(tasks) - 1, (page - 1) * PAGE_SIZE) : min(len(tasks), page * PAGE_SIZE)
    ]
    return tasks, page, max_page


def add_task(text: str) -> None:
    db = get_db()
    db.execute('INSERT INTO task (text) ' 'VALUES (?)', (text,))
    db.commit()

    logger.info(f"Added task: '{text}'")


def finish_task(task_id: int) -> None:
    db = get_db()
    db.execute('UPDATE task SET active = FALSE ' 'WHERE id = (?)', (task_id,))
    db.commit()

    text = db.execute('SELECT * FROM task ' 'WHERE id = (?)', (task_id,)).fetchone()[
        'text'
    ]

    logger.info(f"Finished task: '{text}'")
