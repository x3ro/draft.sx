class JinjaExtensions:
    def __init__(self, app):
        """Registers the custom jinja extensions. `app` must be a Flask app instance."""
        app.jinja_env.globals.update(dict_get=self.get_dict_element)

    @staticmethod
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
