import os
import json
import urllib.parse
import requests
import bleach

from redis import StrictRedis
from flask import Flask, render_template, make_response, abort, request

from draft import markup, assets
from draft.util import HashConverter, gist_page_title, get_dict_element
from draft.jinja_ext import JinjaExtensions
from draft.development import maybe_enable_dev_mode



# ==========================
# Initialize the environemnt
# ==========================

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
assets.setup(app)

# Load custom Jinja functions for Draft
JinjaExtensions(app)

app.url_map.converters['hash'] = HashConverter

DEVELOPMENT = maybe_enable_dev_mode(app)


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
    else:
        content = fetch_and_render(id)

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

    cache_data = process_gist(decoded)
    encoded = json.dumps(cache_data)
    cache.setex(id, CACHE_EXPIRATION, encoded)
    return cache_data

def process_gist(response):
    cache_data = {}
    cache_data['page_title'] = gist_page_title(response)
    cache_data['author'] = get_dict_element(response, 'owner.login', 'anonymous')
    cache_data['description'] = response['description'] or 'No title'

    cache_data['files'] = {}
    for name in response['files']:
        cache_data['files'][name] = markup.render(response['files'][name])

    return cache_data
