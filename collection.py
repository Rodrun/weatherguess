"""Collection system for city weather data.

Simplifies collecting weather data from openweathermap.org by making changes to data needs easy to do.

The 'getlist' is a list of strings with desired data from the weather data. The format of the string:

parent.child

Where parent is a field in the JSON that contains other objects/fields; i.e:

'main.weather' would correspond to:
['main':['weather':'clear']]

So the value returned for that requested field would be 'clear'. Multiple '.' may be used if desired, as well. If
looking for a value that has no sub-fields, simply give the name of the field (i.e. 'temperature').
"""

# Default column values for storing/reading training data
COLUMNS = ("weather.main",
           "main.temp",
           "main.pressure",
           "main.humidity",
           "main.temp_min",
           "main.temp_max",
           "visibility",
           "wind.speed",
           "clouds.all",
           "rain.h3",
           "snow.h3")


class Collection:

    def __init__(self, getlist: list = COLUMNS):
        """
        :param getlist: List of data fields to look for.
        """
        self.getlist = getlist

    def get_weather(self, weather_data, cb=None, default_value=0.):
        """
        Get the weather from a city. default_value is used ONLY for default_callback.
        :param weather_data: Weather JSON data returned from openweathermap.
        :param cb: Callback for each value. Given arguments are: field name and value. Default is default_callback().
        :param default_value: Default value for a field that is None; ONLY used for default_callback.
        :return: Generator of weather data.
        """
        if cb is None:
            cb = Collection.default_callback

        if weather_data is not None:
            for field in self.getlist: # Iterate through desired data
                nodes = field.split(".")
                previous_node = weather_data
                for f in nodes: # Iterate through all the subfields
                    if f in previous_node:
                        previous_node = previous_node[f]
                        if isinstance(previous_node, list): # Use index 0
                            previous_node = previous_node[0]
                    else:
                        previous_node = None
                        
                    if previous_node is None: # Don't look for anything else
                        break

                yield cb(field, previous_node)
        else:
            for field in self.getlist: # Return all fields as None
                yield cb(field, None)

    @staticmethod
    def default_callback(field, value):
        """
        The default callback for get_weather.
        :param field: Name of field.
        :param value: Value of the field.
        :return: If value is None, 0.0, else value.
        """
        return 0.0 if value is None else value

    def get_getlist(self) -> list:
        """
        Get a copy of the getlist.
        :return: Copy of getlist.
        """
        return self.getlist[:]
