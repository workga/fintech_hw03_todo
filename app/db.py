import sqlite3

import click
from flask import Flask, current_app, g
from flask.cli import with_appcontext

from app.config import DB_FILENAME, SCHEMA_FILENAME


def dict_factory(cursor: sqlite3.Cursor, row: sqlite3.Row):
    d = {}
    for i, col in enumerate(cursor.description):
        d[col[0]] = row[i]
    return d


def get_db() -> sqlite3.Connection:
    if not hasattr(g, 'db_connection'):
        conn = sqlite3.connect(DB_FILENAME)
        conn.row_factory = dict_factory
        setattr(g, 'db_connection', conn)

    return g.db_connection


def close_db(error) -> None:
    if hasattr(g, 'db_connection'):
        g.db_connection.close()

    if error:
        current_app.logger.error(error)


def init_db(filename=SCHEMA_FILENAME) -> None:
    db = get_db()

    with open(filename, encoding='utf8') as f:
        db.executescript(f.read())


def init_app(app: Flask) -> None:
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


@click.command('init-db')
@with_appcontext
def init_db_command() -> None:
    init_db()
    click.echo('Initialized the database.')
