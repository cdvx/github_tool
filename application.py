from flask import Flask
from flask_dance.contrib.github import make_github_blueprint, github

# from flask_sqlalchemy import SQLAlchemy
from config import config
from api.utils.db import db


# Import Blueprints
from api.views import user_app


def create_app(ENV):
    app = Flask(__name__)
    app.config.from_object(config.get(ENV))
    blueprint = make_github_blueprint(client_id=config.get(ENV).GITHUB_CLIENT_ID,
                                    client_secret=config.get(ENV).GITHUB_CLIENT_SECRET
      )
    app.register_blueprint(blueprint, url_prefix="")

    # setup_db
    db.init_app(app)

    # Register Blueprints
    app.register_blueprint(user_app)
    
    return app

