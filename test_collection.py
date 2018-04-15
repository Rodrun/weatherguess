import unittest
import requests

from collection import Collection

class TestCollection(unittest.TestCase):

    def setUp(self):
        # Get the sample JSON data
        self.data = requests.get("http://samples.openweathermap.org/data/2.5/weather?zip=94040,us&appid=b6907d289e10d714a6e88b30761fae22").json()
        self.coll = Collection(getlist=["weather.main", "main.temp", "clouds.all", "doesntExist"])
        self.dcoll = Collection()

    def test_detect_none(self):
        """
        Test if get_weather returns a list of the default value when given None.
        """
        self.assertCountEqual([x for x in self.coll.get_weather(None)],
                              [0. for i in range(0, len(self.coll.get_getlist()))])

    def test_get_weather(self):
        """
        Test if get_weather functions correctly.
        """
        data = [x for x in self.coll.get_weather(self.data)]

        self.assertIsInstance(data[0], str)
        self.assertIsInstance(data[1], float)
        self.assertIsInstance(data[2], int)
        self.assertEqual(data[3], 0.)

    def test_get_weather_defaults(self):
        """
        Test if get_weather functions correctly using the default getlist.
        """
        data = [x for x in self.dcoll.get_weather(self.data)]
        self.assertIsNotNone(data)
        print(data)
