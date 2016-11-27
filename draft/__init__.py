import os


from flask import Flask
from draft.development import maybe_enable_dev_mode

from . import jinja
from . import util

import draft.jinja
import draft.util

from redis import StrictRedis

GITHUB_CLIENT_ID = os.environ.get('GITHUB_CLIENT_ID')
GITHUB_CLIENT_SECRET = os.environ.get('GITHUB_CLIENT_SECRET')

GITHUB_AUTH_PARAMS = {'client_id': GITHUB_CLIENT_ID,
               'client_secret': GITHUB_CLIENT_SECRET}

CACHE_EXPIRATION = 120  # seconds
redis = StrictRedis(host='redis')
PORT = 5000

STATIC_URL = '/static/'

# ==========================
# Initialize the app
# ==========================

app = Flask(__name__)
DEVELOPMENT = maybe_enable_dev_mode(app)

# Load custom Jinja functions for Draft
jinja.Extensions(app)

app.url_map.converters['hash'] = util.HashConverter



import draft.views


# ==========================
# Routes
# ==========================



# def fetch_and_render(id):
#     """Fetch and render a post from the Github API"""
#     r = requests.get('https://api.github.com/gists/{}'.format(id),
#                      params=AUTH_PARAMS)
#     if r.status_code != 200:
#         app.logger.warning('Fetch {} failed: {}'.format(id, r.status_code))
#         return None

#     try:
#         decoded = r.json().copy()
#     except ValueError:
#         app.logger.error('Fetch {} failed: unable to decode JSON response'.format(id))
#         return None

#     cache_data = process_gist(decoded)
#     encoded = json.dumps(cache_data)
#     cache.setex(id, CACHE_EXPIRATION, encoded)
#     return cache_data


