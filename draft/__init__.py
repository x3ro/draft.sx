import os
import json
import urllib.parse
import requests
import bleach

from redis import StrictRedis
from flask import Flask, render_template, make_response, abort, request

from draft import markup
from draft.util import HashConverter
from draft.jinja_ext import JinjaExtensions



# ==========================
# Initialize the environemnt
# ==========================

DEVELOPMENT = 'DEVELOPMENT' in os.environ

GITHUB_CLIENT_ID = os.environ.get('GITHUB_CLIENT_ID')
GITHUB_CLIENT_SECRET = os.environ.get('GITHUB_CLIENT_SECRET')

AUTH_PARAMS = {'client_id': GITHUB_CLIENT_ID,
               'client_secret': GITHUB_CLIENT_SECRET}

CACHE_EXPIRATION = 120  # seconds
cache = StrictRedis()
PORT = 5000

STATIC_URL = '/static/'



# ==========================
# Initialize the app
# ==========================

app = Flask(__name__)

markup = markup.Markup(app)

# Load custom Jinja functions for Draft
JinjaExtensions(app)

app.url_map.converters['hash'] = HashConverter



# ==========================
# Routes
# ==========================

@app.route('/')
def homepage():
    return render_gist('691fe85788524e6627fa')

@app.route('/<hash:id>')
def render_gist(id):
    content = cache.get(id)
    if content:
        content = json.loads(content.decode("utf-8"))


    return render_template(
        'gist.html',
        gist_id = id,
        STATIC_URL = STATIC_URL,
        content = content,
        monitoring = {
            'google_analytics': os.environ.get('GOOGLE_ANALYTICS'),
            'pingdom': os.environ.get('PINGDOM')
        }
    )

@app.route('/embed_gist/<user>/<id>')
def embed_gist(user, id):
    embed_url = 'https://gist.github.com/{}/{}.js'.format(user, id)
    r = requests.get(embed_url)
    if r.status_code != 200:
        app.logger.warning('Fetching gist embed script for id {} failed: {}'.format(id, r.status_code))

    resp = make_response(r.text, 200)
    return resp

@app.route('/<hash:id>/content')
def gist_contents(id):
    cache_hit = True
    content = cache.get(id)
    if not content:
        cache_hit = False
        content = fetch_and_render(id)
    if content is None:
        abort(404)
    resp = make_response(content, 200)
    resp.headers['Content-Type'] = 'application/json'
    resp.headers['X-Cache-Hit'] = cache_hit
    resp.headers['X-Expire-TTL-Seconds'] = cache.ttl(id)
    return resp


def fetch_and_render(id):
    """Fetch and render a post from the Github API"""
    r = requests.get('https://api.github.com/gists/{}'.format(id),
                     params=AUTH_PARAMS)
    if r.status_code != 200:
        app.logger.warning('Fetch {} failed: {}'.format(id, r.status_code))
        return None

    try:
        decoded = r.json().copy()
    except ValueError:
        app.logger.error('Fetch {} failed: unable to decode JSON response'.format(id))
        return None

    for f in decoded['files'].values():
        f = markup.render(f)

    encoded = json.dumps(decoded)
    cache.setex(id, CACHE_EXPIRATION, encoded)
    return encoded
