from flask import Blueprint, Response, redirect, render_template, request

from app.todo import manager

bp = Blueprint('todo', __name__)


@bp.route('/tasks', methods=['GET', 'POST'])
def tasks():
    if request.method == 'GET':
        active_filter = request.args.get('active_filter', 'all', str)
        text_filter = request.args.get('text_filter', '', str)
        page = request.args.get('page', 1, int)

        tasks_list, page, max_page = manager.find_tasks(
            active_filter, text_filter, page
        )

        return render_template(
            'todo/tasks.html',
            tasks=tasks_list,
            text_filter=text_filter,
            page=page,
            max_page=max_page,
        )

    if request.method == 'POST':
        task_text = request.form['task_text']

        manager.add_task(task_text)

        return redirect(request.referrer)

    return Response(status=405)


@bp.route('/tasks/finish', methods=['POST'])
def tasks_finish():
    task_id = request.form.get('task_id', type=int)

    manager.finish_task(task_id)

    return redirect(request.referrer)
