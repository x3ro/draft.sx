import json
import requests

from . import app, redis, GITHUB_AUTH_PARAMS, CACHE_EXPIRATION, markup
from .util import get_dict_element

def get(id):
    content = redis.get(id)
    if content:
        app.logger.debug("Found in cache {}".format(id))
        return json.loads(content.decode("utf-8"))
    else:
        return cache(id, render(api_fetch(id)))

def cache(id, pgist):
    if not pgist:
        return None

    encoded = json.dumps(pgist)
    redis.setex(id, CACHE_EXPIRATION, encoded)
    return pgist


def api_fetch(id):
    app.logger.debug("Fetching gist {}".format(id))

    r = requests.get('https://api.github.com/gists/{}'.format(id), params=GITHUB_AUTH_PARAMS)
    if r.status_code != 200:
        app.logger.warning('Fetch {} failed: {}'.format(id, r.status_code))
        return None

    try:
        decoded = r.json().copy()
    except ValueError:
        app.logger.error('Fetch {} failed: unable to decode JSON response'.format(id))
        return None

    return decoded


def page_title(gist):
    """Generates the page title (string) for the gist (dict)"""

    title = get_dict_element(gist, 'description', 'Untitled')
    if "draft.sx" in title:
        return title
    else:
        return "draft.sx &#183; %s" % (title)

def render(gist):
    """
    Renders a GitHub API response (contained markup and additional fields).

    Arguments:
        gist (dict): GitHub API response

    Returns:
        A dict with the processed data
    """

    if not gist:
        return None

    data = {}
    data['page_title'] = page_title(gist)
    data['author'] = get_dict_element(gist, 'owner.login', 'anonymous')
    data['author_url'] = get_dict_element(gist, 'owner.html_url', 'javascript:void(0);')
    data['description'] = gist['description'] or 'No title'

    data['files'] = {}
    for name in gist['files']:
        data['files'][name] = markup.render(gist['files'][name])

    return data
