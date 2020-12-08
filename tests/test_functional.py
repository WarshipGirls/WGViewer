import unittest

from src.data.__auto_gen__ import start_data_generator
from src.utils.__auto_gen__ import start_utils_generator


class FunctionalTests(unittest.TestCase):

    def test_data_init_generator(self):
        self.assertEqual(start_data_generator(), True)

    def test_utils_init_generator(self):
        self.assertEqual(start_utils_generator(), True)


if __name__ == '__main__':
    unittest.main()
