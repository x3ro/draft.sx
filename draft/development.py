import os

from werkzeug.contrib.profiler import ProfilerMiddleware
from flask.ext.compress import Compress

def maybe_enable_dev_mode(app):
    if not 'DEVELOPMENT' in os.environ:
        return False

    Compress(app)                                      # Enable gzip
    app.config['ASSETS_DEBUG'] = True                  # Don't pack assets (css/js)
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app)    # Enable profiler

    return True
