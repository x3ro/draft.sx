from draft.util import get_dict_element

class Extensions:
    def __init__(self, app):
        """Registers the custom jinja extensions. `app` must be a Flask app instance."""
        app.jinja_env.globals.update(dict_get=get_dict_element)


