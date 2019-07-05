from flask import (render_template_string,
                   render_template, jsonify,
                   request, g, session, redirect,
                   url_for, Blueprint)
import requests, json
from flask_github import GitHub
from api.utils.db import db
from .models import User
from config import Config
from flask_dance.contrib.github import github

try:
    from urllib.parse import urlencode, parse_qs
except ImportError:
    from urllib import urlencode
    from urlparse import parse_qs



user_app = Blueprint('user_app', __name__)
github_config_object = {
    'GITHUB_CLIENT_ID': Config.GITHUB_CLIENT_ID,
    'GITHUB_CLIENT_SECRET': Config.GITHUB_CLIENT_SECRET
}

setattr(user_app, 'config', github_config_object)


@user_app.route('/')
def index():
    if g.user:
        
        return render_template('index.html', user=g.user)
    return render_template('index.html', user=g.user)

from functools import wraps

def authorized_handler(f):
    """
    Decorator for the route that is used as the callback for authorizing
    with GitHub. This callback URL can be set in the settings for the app
    or passed in during authorization.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'code' in request.args:
            data = _handle_response()
        else:
            data = _handle_invalid_response()
        return f(*((data,) + args), **kwargs)
    return decorated

@user_app.route('/github-callback')
@authorized_handler
def authorized(access_token):
    next_url = request.args.get('next') or url_for('user_app.index')
    if access_token is None:
        return redirect(next_url)

    user = User(access_token)
    user.github_access_token = access_token
    headers = {
        "Authorization": f"token {access_token}"
    }
    
    github_user = github.get('/user', headers=headers).json()
    
    user.github_id = github_user['id']
    user.email = github_user['email']
    user.username = github_user['name']
    user.github_login = github_user['login']
    user.image = github_user['avatar_url']
    
    user_exists =check_user_exists(user.username)
    if not user_exists:
        db.session.add(user)

    else:
        user.update_(**{
                "github_access_token": access_token,
                "username": user.username
            })
    g.user = user
    db.session.commit()
    session['user_id'] = user.username or user.github_login

    return redirect(next_url)
    
def _handle_invalid_response():
        pass

def _handle_response():
    """
    Handles response after the redirect to GitHub. This response
    determines if the user has allowed the this application access. If we
    were then we send a POST request for the access_key used to
    authenticate requests to GitHub.
    """
    params = {
        'code': request.args.get('code'),
        'client_id': Config.GITHUB_CLIENT_ID,
        'client_secret': Config.GITHUB_CLIENT_SECRET
    }
    url = "https://github.com/login/oauth/access_token"
    response = requests.post(url, data=params)
    data = parse_qs(response.content)
    for k, v in data.items():
        if len(v) == 1:
            data[k] = v[0]
    token = data.get(b'access_token', None)
    if token is not None:
        token = token.decode('ascii')
    return token

def check_user_exists(username):
    user = User.query.filter_by(username=username).first()
    return user



@user_app.route('/login')
def login():

    if not github.authorized:
        url = f"https://github.com/login/oauth/authorize?client_id={Config.GITHUB_CLIENT_ID}"
        return redirect(url)

    account_info=github.get("/user")
    if account_info.ok:
        return redirect(url_for("user_app.index"))
    else:
        return "Already logged in"


@user_app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('user_app.index'))


@user_app.route('/user')
def user():
    return render_template('index.html', user=g.user)


@user_app.route('/repo')
def repo():
    headers = {
        "Authorization": f"token {g.user.github_access_token}"
    }
    repos = github.get(f'/users/{g.user.github_login}/repos', headers=headers).json()

    rep = [to_rep(repo) for repo in repos]
    return render_template('repos.html', user=g.user, repos=rep)

def to_rep(obj):
    temp = {
        'name': obj['name'],
        'description': obj['description'] if  obj['description'] else 'No description available',
        'clone_url': obj['clone_url'],
        'full_name': obj['full_name']
    }
    return temp
