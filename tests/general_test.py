import os
import unittest

from tests.utils import get_project_root

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


class FileIntegrityTests(unittest.TestCase):

    def test_requirements_exists(self):
        _dir = ROOT_DIR.joinpath('requirements.txt')
        self.assertEqual(_dir.exists(), True)
        self.assertEqual(_dir.is_dir(), False)

    def test_license_exists(self):
        _dir = ROOT_DIR.joinpath('LICENSE')
        self.assertEqual(_dir.exists(), True)
        self.assertEqual(_dir.is_dir(), False)

    def test_readme_exists(self):
        _dir = ROOT_DIR.joinpath('README.md')
        self.assertEqual(_dir.exists(), True)
        self.assertEqual(_dir.is_dir(), False)

    def test_win_build_exists(self):
        _dir = ROOT_DIR.joinpath('win_build.bat')
        self.assertEqual(_dir.exists(), True)
        self.assertEqual(_dir.is_dir(), False)


if __name__ == '__main__':
    unittest.main()
