import os
import unittest

from tests.utils import get_project_root
from src.data.__auto_gen__ import start_generator

ROOT_DIR = get_project_root()


def is_dir_empty(path):
    return len(os.listdir(path)) == 0


class DirectoryIntegrityTests(unittest.TestCase):

    def test_screenshots_dir_exists(self):
        _dir = ROOT_DIR.joinpath('screenshots')

        self.assertEqual(_dir.exists(), True)
        self.assertEqual(_dir.is_dir(), True)
        self.assertEqual(is_dir_empty(_dir), False)

    def test_zip_dir_exists(self):
        _dir = ROOT_DIR.joinpath('zip')

        self.assertEqual(_dir.exists(), True)
        self.assertEqual(_dir.is_dir(), True)
        self.assertEqual(is_dir_empty(_dir), False)

    def test_tools_dir_exists(self):
        _dir = ROOT_DIR.joinpath('tools')

        self.assertEqual(_dir.exists(), True)
        self.assertEqual(_dir.is_dir(), True)
        self.assertEqual(is_dir_empty(_dir), False)

    def test_assets_dir_exists(self):
        _dir = ROOT_DIR.joinpath('assets')

        self.assertEqual(_dir.exists(), True)
        self.assertEqual(_dir.is_dir(), True)
        self.assertEqual(is_dir_empty(_dir), False)

    def test_tests_dir_exists(self):
        _dir = ROOT_DIR.joinpath('tests')

        self.assertEqual(_dir.exists(), True)
        self.assertEqual(_dir.is_dir(), True)
        self.assertEqual(is_dir_empty(_dir), False)


class FunctionalTests(unittest.TestCase):

    def test_data_init_generator(self):
        self.assertEqual(start_generator(), True)


if __name__ == '__main__':
    unittest.main()
