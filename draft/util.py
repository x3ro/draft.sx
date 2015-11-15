from werkzeug.routing import BaseConverter
from draft.jinja_ext import JinjaExtensions

class HashConverter(BaseConverter):
    def __init__(self, url_map):
        super(HashConverter, self).__init__(url_map)
        self.regex = r'[a-fA-F\d]+'


def gist_page_title(content):
    title = "Untitled"

    gist_title = JinjaExtensions.get_dict_element(content, 'description', 'Untitled')
    if len(gist_title) > 0:
        title = gist_title

    if "draft.sx" in gist_title:
        return gist_title
    else:
        return "draft.sx &#183; %s" % (title)
