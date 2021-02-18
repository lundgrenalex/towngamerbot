import unittest
from lib.storage import cities


class TestStringMethods(unittest.TestCase):

    def test_get_random(self):
        random_city = cities.get_random()
        self.assertEqual(type(random_city), str)

if __name__ == '__main__':
    unittest.main()
