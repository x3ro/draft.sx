from werkzeug.routing import BaseConverter

class HashConverter(BaseConverter):
    def __init__(self, url_map):
        super(HashConverter, self).__init__(url_map)
        self.regex = r'[a-fA-F\d]+'
