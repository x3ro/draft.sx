from flask.ext.assets import Environment, Bundle

def setup(app):
    assets = Environment(app)

    scss = Bundle('../sass/pixyll.scss', filters=['libsass'], output='css/packed.css')
    assets.register('scss_all', scss)
