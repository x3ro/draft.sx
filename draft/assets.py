from flask.ext.assets import Environment, Bundle

def setup(app):
    assets = Environment(app)

    js = Bundle('js/jquery-2.1.4.js', 'js/draft.js', 'js/embed_gist.js',
                filters='jsmin', output='js/packed.js')
    assets.register('js_all', js)

    scss = Bundle('../sass/pixyll.scss', filters=['libsass', 'cssmin'], output='css/packed.css')
    assets.register('scss_all', scss)