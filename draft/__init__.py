import os
import json
import urllib.parse

from redis import StrictRedis
from markdown import markdown
import requests
import bleach

from draft.util import HashConverter

from flask import Flask, render_template, make_response, abort, request
app = Flask(__name__)

HEROKU = 'HEROKU' in os.environ

GITHUB_CLIENT_ID = os.environ.get('GITHUB_CLIENT_ID')
GITHUB_CLIENT_SECRET = os.environ.get('GITHUB_CLIENT_SECRET')

AUTH_PARAMS = {'client_id': GITHUB_CLIENT_ID,
               'client_secret': GITHUB_CLIENT_SECRET}

if HEROKU:
    urlparse.uses_netloc.append('redis')
    redis_url = urlparse.urlparse(os.environ['REDISCLOUD_URL'])
    print(redis_url)
    cache = StrictRedis(host=redis_url.hostname,
                        port=redis_url.port,
                        password=redis_url.password)
    PORT = int(os.environ.get('PORT', 5000))
else:
    cache = StrictRedis()  # local development
    PORT = 5000

STATIC_URL = '/static/'
CACHE_EXPIRATION = 1  # seconds

RENDERABLE = (u'Markdown', u'Text', u'Literate CoffeeScript', None)

ALLOWED_TAGS = [
    "a", "abbr", "acronym", "b", "blockquote", "code", "em", "i", "li", "ol", "strong",
    "ul", "br", "img", "span", "div", "pre", "p", "dl", "dd", "dt", "tt", "cite", "h1",
    "h2", "h3", "h4", "h5", "h6", "table", "col", "tr", "td", "th", "tbody", "thead",
    "colgroup", "hr",
]

ALLOWED_ATTRIBUTES = {
    "a": ["href", "title"],
    "acronym": ["title"],
    "abbr": ["title"],
    "img": ["src"],
}

app.url_map.converters['hash'] = HashConverter

@app.route('/oauth')
def oauth():
    app.logger.warning("Method: {}".format(request.method))
    app.logger.warning("Args: {}".format(request.args))
    return(u"oauth")

@app.route('/')
def homepage():
    return render_gist(6274616)


@app.route('/<hash:id>')
def render_gist(id):
    return render_template('gist.html', gist_id=id, STATIC_URL=STATIC_URL)

@app.route('/embed_gist/<int:id>')
def embed_gist(id):
    embed_url = 'https://gist.github.com/x3ro/{}.js'.format(id)
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
        if f['language'] in RENDERABLE:
            app.logger.debug('{}: renderable!'.format(f['filename']))
            f['rendered'] = markdown(f['content'], extensions=['attr_list', 'fenced_code', 'codehilite'])

    encoded = json.dumps(decoded)
    cache.setex(id, CACHE_EXPIRATION, encoded)
    return encoded



