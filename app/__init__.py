from flask import Flask

from app import db
from app.todo import logger, view


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    db.init_app(app)

    app.register_blueprint(view.bp)
    app.add_url_rule('/tasks', endpoint='tasks')

    logger.init()

    return app
