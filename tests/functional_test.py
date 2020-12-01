import unittest

from src.data.__auto_gen__ import start_generator


class FunctionalTests(unittest.TestCase):

    def test_data_init_generator(self):
        self.assertEqual(start_generator(), True)


if __name__ == '__main__':
    unittest.main()
