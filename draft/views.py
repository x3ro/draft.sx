import os

from . import app, STATIC_URL
from . import gist

from flask import render_template, redirect

@app.route('/')
def homepage():
    return render_gist('b5807b9c969cef7420e0e6d4884aafd3')

@app.route('/impressum')
def render_impressum():
    return render_template('impressum.html')

@app.route('/<hash:id>')
def render_gist(id):
    return redirect("https://gist.github.com/" + id, code=301)
