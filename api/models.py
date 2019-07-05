from api.utils.db import db
from flask import request


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    github_access_token = db.Column(db.String(255))
    github_id = db.Column(db.Integer)
    github_login = db.Column(db.String(255))
    username = db.Column(db.String(255))
    email = db.Column(db.String(255))
    image = db.Column(db.String(255))

    def __init__(self, github_access_token):
        self.github_access_token = github_access_token


    def update_(self, **kwargs):
        """
        update entries
        """
        username, github_access_token = kwargs.get('username'), kwargs.get('github_access_token')
        sql = """UPDATE users SET github_access_token = %s 
                 WHERE username = %s"""
        if username and github_access_token:
            db.engine.execute(sql, (github_access_token, username))
        # db.session.commit()