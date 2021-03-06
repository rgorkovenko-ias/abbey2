import re
import functools
import flask
import mistune


def login_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in flask.session:
            return flask.redirect(
                flask.url_for('login_page', next=flask.request.url))
        return f(*args, **kwargs)
    return decorated_function


def no_cache(resp):
    endpoint = flask.request.endpoint
    if (endpoint is not None) and (endpoint not in ('static')):
        resp.headers.set(
            'Cache-Control',
            'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
        resp.headers.set('Expires', 'Fri, 20 Nov 1981 08:52:00 GMT')
        resp.headers.set('Pragma', 'no-cache')
    return resp


def markdown(text):
    if 'markdown' not in flask.g:
        flask.g.markdown = mistune.Markdown(
            renderer=mistune.Renderer(escape=False))
    md = flask.g.markdown
    return md(text)


def canonical():
    return re.sub(r'^http\:', 'https:', flask.request.base_url)
