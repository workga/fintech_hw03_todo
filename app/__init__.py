import logging
from flask import Flask

from app.config import LOGGING_FILENAME

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    from app import db
    db.init_app(app)

    from app.todo import view
    app.register_blueprint(view.bp)
    app.add_url_rule('/tasks', endpoint='tasks')

    # logging.getLogger('todo').
    # logging.basicConfig(filename=LOGGING_FILENAME, level=logging.INFO)

    return app