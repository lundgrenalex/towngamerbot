import unittest
from src.domain.city import City


class TestAnswerModel(unittest.TestCase):

    def test_model(self):
        city = City(city='Moscow', state='Moscow', region='Central', population=1234342)
        self.assertEqual(type(city.city), str)
        self.assertEqual(type(city.state), str)
        self.assertEqual(type(city.region), str)
        self.assertEqual(type(city.population), int)

if __name__ == '__main__':
    unittest.main()
