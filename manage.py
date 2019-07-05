from flask import Flask, g, session, jsonify, flash, redirect, url_for

from config import config, AppConfig
from flask_script import Manager, Server, Shell
from flask_migrate import Migrate, MigrateCommand
import os

from api.models import User
from flask_github import GitHubError
from api.utils.db import db

from application import create_app


app = create_app(os.getenv('FLASK_ENV', 'development'))
migrate = Migrate(app, db)
manager = Manager(app)

@app.errorhandler(GitHubError)
def jumpship(error):
    session.pop('user_id', None)
    flash('Something bad happened. Please try again?', 'error')
    return redirect(url_for('user_app.index'))

@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        user_id = session['user_id']
        g.user = User.query.filter_by(username=user_id).first() if user_id else None


@app.after_request
def after_request(response):
    db.session.remove()
    return response


def _make_context():
    return dict(app=app, db=db)


@manager.command
def test():
    pytest.main(["-s", "tests/"])


@manager.command
def test_coverage():
    pytest.main(["--cov=.", "tests/"])


@manager.command
def test_cov_report():
    pytest.main(["--cov-report", "html:cov_html",
                 "--cov=.", "tests/"])


# Turn on reloader
manager.add_command('runserver', Server(
    use_reloader=True,
    host=os.getenv('IP', '0.0.0.0'),
    port=int(os.getenv('PORT', 5000))
))

# Migrations
manager.add_command('db', MigrateCommand)


manager.add_command("shell", Shell(make_context=_make_context))



if __name__ == '__main__':
    manager.run()