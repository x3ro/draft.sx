import emoji
import emoji_unicode
import re
import bleach

from markdown import markdown
from . import app

RENDERABLE = (u'Markdown', u'Text', u'Literate CoffeeScript')

ALLOWED_TAGS = [
    "a", "abbr", "acronym", "b", "blockquote", "code", "em", "i", "li", "ol", "strong",
    "ul", "br", "img", "span", "div", "pre", "p", "dl", "dd", "dt", "tt", "cite", "h1",
    "h2", "h3", "h4", "h5", "h6", "table", "col", "tr", "td", "th", "tbody", "thead",
    "colgroup", "hr", "footer", "del", "ins"
]

ALLOWED_ATTRIBUTES = {
    "*": ["class", "title"],
    "a": ["href"],
    "img": ["src", "alt"],
}

EXTENSIONS = ['attr_list', 'fenced_code', 'codehilite', 'def_list', 'footnotes',
              'tables', 'admonition']

EMOJI_PATTERN = re.compile(emoji_unicode.RE_PATTERN_TEMPLATE)

def render(content):
    """
    Convert given markup content to HTML.

    `content` should be a `dict` containing the keys `language` and `content`, whereas
    `language` is the type of markup and `content` contains markup of said type.

    Returns the `dict` with an additional key `rendered` (not a copy! the input is
    modified!)
    """
    if content['language'] in RENDERABLE:
        app.logger.debug('{}: renderable!'.format(content['filename']))
        content['rendered'] = emoji.emojize(content['content'], use_aliases=True)
        content['rendered'] = re.sub(EMOJI_PATTERN, emoji_match_handler, content['rendered'])
        content['rendered'] = markdown(content['rendered'], extensions=EXTENSIONS)
        content['rendered'] = bleach.clean(
            content['rendered'],
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES
        )
        content['rendered'] = bleach.linkify(content['rendered'])

    return content

def emoji_match_handler(m):
    """
    Matches unicode emoji and translates them to their SVG representation.
    See https://github.com/nitely/emoji-unicode for more info
    """
    e = emoji_unicode.Emoji(unicode=m.group('emoji'))
    return u'<img src="static/img/emoji/{filename}.svg" alt="{raw}" class="emoji">'.format(
        filename=e.code_points,
        raw=e.unicode
    )
