import unittest
from app.geo_functions import geocode_city

class TestGeocodeCity(unittest.TestCase):
    def test_geocode_city_success(self):

        result = geocode_city("Москва")

        self.assertIsInstance(result, dict)
        self.assertIn("lat", result)
        self.assertIn("lng", result)

        self.assertIsInstance(result["lat"], float)
        self.assertIsInstance(result["lng"], float)

    def test_geocode_city_no_data(self):
        result = geocode_city("NonexistentCity")

        self.assertIsNone(result)
if __name__ == '__main__':
    unittest.main()
