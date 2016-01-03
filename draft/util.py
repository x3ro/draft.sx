from werkzeug.routing import BaseConverter

class HashConverter(BaseConverter):
    def __init__(self, url_map):
        super(HashConverter, self).__init__(url_map)
        self.regex = r'[a-fA-F\d]+'

def get_dict_element(someDict, stringPath, defaultValue):
    """
    Return the value pointed to by `stringPath` in `someDict`. If it does not exist,
    return `defaultValue` instead.

    Arguments:
    someDict    --  Must be of type dict :)
    stringPath  --  Must be a string of the format 'firstkey.secondkey.thirdkey....'
                    May have as many segments as desired.
    """
    path = stringPath.split('.')

    for step in path:
        if not type(someDict) is dict:
            return defaultValue

        if step in someDict:
            someDict = someDict[step]
        else:
            return defaultValue

    return someDict
