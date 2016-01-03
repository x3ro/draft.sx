import os

from . import app, STATIC_URL
from . import gist

from flask import render_template

@app.route('/')
def homepage():
    return render_gist('691fe85788524e6627fa')

@app.route('/<hash:id>')
def render_gist(id):
    _gist = gist.get(id)
    return render_template(
        'gist.html',
        gist_id = id,
        STATIC_URL = STATIC_URL,
        content = _gist,
        monitoring = {
            'google_analytics': os.environ.get('GOOGLE_ANALYTICS')
        }
    )
