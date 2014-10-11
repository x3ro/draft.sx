from markdown import markdown

class Markup:
    RENDERABLE = (u'Markdown', u'Text', u'Literate CoffeeScript')

    # XXX This isn't used anymore. Should it be re-enabled with current MD parser?
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

    EXTENSIONS = ['attr_list', 'fenced_code', 'codehilite']

    def __init__(self, app):
        """`app` must be a Flask app instance."""
        self.app = app

    def render(self, content):
        """
        Convert given markup content to HTML.

        `content` should be a `dict` containing the keys `language` and `content`, whereas
        `language` is the type of markup and `content` contains markup of said type.

        Returns the `dict` with an additional key `rendered` (not a copy! the input is
        modified!)
        """
        if content['language'] in self.RENDERABLE:
            self.app.logger.debug('{}: renderable!'.format(content['filename']))
            content['rendered'] = markdown(content['content'], extensions=self.EXTENSIONS)

        return content
