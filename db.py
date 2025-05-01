import sqlite3
import os
import shutil
from datetime import datetime

import click
from flask import Flask, current_app, g

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db
    
def add_user(username, password):
    db = get_db()
    db.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    db.commit()

def get_user(username):
    db = get_db()
    return db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables + delete and remake uploads folder"""
    folder_path = 'static/uploads'
    if os.path.exists(folder_path):
        print("folder exists")
        shutil.rmtree(folder_path)
    os.makedirs(folder_path)
    init_db()
    click.echo('Initialized the database.')


sqlite3.register_converter(
    "timestamp", lambda v: datetime.fromisoformat(v.decode())
)

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)





