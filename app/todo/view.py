from flask import (
    Blueprint,
    redirect,
    render_template,
    request, 
    url_for,
    # current_app
)
# import logging

from app.todo import manager

bp = Blueprint('todo', __name__)

@bp.route('/tasks', methods=['GET', 'POST'])
def tasks():
    if request.method == 'GET':
        active_filter = request.args.get("active_filter", "all")
        text_filter = request.args.get("text_filter", "")
        page = request.args.get("page", 1, int)

        tasks, page, max_page = manager.find_tasks(active_filter, text_filter, page)

        return render_template(
            'todo/tasks.html',
            tasks=tasks,
            text_filter=text_filter,
            page=page,
            max_page=max_page
        )

    if request.method == 'POST':
        task_text = request.form['task_text']

        manager.add_task(task_text)
        # current_app.logger.info(f"Added task: '{task_text}'")
        # logging.info(f"Added task: '{task_text}'")

        return redirect(url_for('tasks'))


@bp.route('/tasks/finish', methods=['POST'])
def tasks_finish():
        task_id = request.form['task_id']
        task_text = manager.find_task_by_id(task_id)["text"]

        manager.finish_task(task_id)
        # current_app.logger.info(f"Finished task: '{task_text}'")
        # logging.info(f"Added task: '{task_text}'")

        return redirect(url_for('tasks'))