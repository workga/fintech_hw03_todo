import math

from app.config import PAGE_SIZE
from app.db import get_db

def page_count(tasks_count):
    if tasks_count == 0:
        return 1
    elif tasks_count % PAGE_SIZE == 0:
        return tasks_count // PAGE_SIZE
    else:
        return tasks_count // PAGE_SIZE + 1

def find_tasks(active_filter, text_filter, page):
    db = get_db()
    tasks = db.execute(
        'SELECT * FROM task '
        'ORDER BY created DESC ',
    ).fetchall()

    if active_filter == "active":
        tasks = [t for t in tasks if t["active"]]
    elif active_filter == "finished":
        tasks = [t for t in tasks if not t["active"]]
    
    if text_filter:
        tasks = [t for t in tasks if text_filter in t["text"]]

    max_page = page_count(len(tasks))
    page = min(page, max_page)

    return tasks[
        min(len(tasks) - 1, (page - 1) * PAGE_SIZE) :
        min(len(tasks), page * PAGE_SIZE)
    ], page, max_page

def find_task_by_id(id):
    db = get_db()
    task = db.execute(
        'SELECT * FROM task '
        'WHERE id = (?)',
        (id, )
    ).fetchone()

    return task

def add_task(text):
    db = get_db()
    db.execute(
        'INSERT INTO task (text) '
        'VALUES (?)',
        (text,)
    )
    db.commit()

def finish_task(id):
    db = get_db()
    db.execute(
        'UPDATE task SET active = FALSE '
        'WHERE id = (?)',
        (id,)
    )
    db.commit()