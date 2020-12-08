import os
import unittest

from packaging import version

from src.general import get_app_version
from tests.utils import get_project_root, get_file_size

ROOT_DIR = get_project_root()


def is_dir_empty(path):
    return len(os.listdir(path)) == 0


class TestDirectoryIntegrity(unittest.TestCase):

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

    def test_src_dir_exists(self):
        _dir = ROOT_DIR.joinpath('src')
        self.assertEqual(_dir.exists(), True)
        self.assertEqual(_dir.is_dir(), True)
        self.assertEqual(is_dir_empty(_dir), False)

    def test_docs_dir_exists(self):
        _dir = ROOT_DIR.joinpath('docs')
        self.assertEqual(_dir.exists(), True)
        self.assertEqual(_dir.is_dir(), True)
        self.assertEqual(is_dir_empty(_dir), False)


class TestFileIntegrity(unittest.TestCase):

    def test_requirements_exists(self):
        _file = ROOT_DIR.joinpath('requirements.txt')
        self.assertEqual(_file.exists(), True)
        self.assertEqual(_file.is_dir(), False)
        self.assertNotEqual(get_file_size(_file), 0)

    def test_license_exists(self):
        _file = ROOT_DIR.joinpath('LICENSE')
        self.assertEqual(_file.exists(), True)
        self.assertEqual(_file.is_dir(), False)
        self.assertNotEqual(get_file_size(_file), 0)

    def test_readme_exists(self):
        _file = ROOT_DIR.joinpath('README.md')
        self.assertEqual(_file.exists(), True)
        self.assertEqual(_file.is_dir(), False)
        self.assertNotEqual(get_file_size(_file), 0)

    def test_win_build_exists(self):
        _file = ROOT_DIR.joinpath('win_build.bat')
        self.assertEqual(_file.exists(), True)
        self.assertEqual(_file.is_dir(), False)
        self.assertNotEqual(get_file_size(_file), 0)

    def test_disclaimer_exists(self):
        _file = ROOT_DIR.joinpath('DISCLAIMER.md')
        self.assertEqual(_file.exists(), True)
        self.assertEqual(_file.is_dir(), False)
        self.assertNotEqual(get_file_size(_file), 0)

    def test_version_file_valid(self):
        _file = ROOT_DIR.joinpath('version')
        self.assertEqual(_file.exists(), True)
        self.assertEqual(_file.is_dir(), False)
        self.assertNotEqual(get_file_size(_file), 0)
        with open(_file, 'r') as f:
            ver = f.read()
        self.assertEqual(ver, get_app_version())
        self.assertEqual(type(version.parse(ver)), version.Version)

    def test_banner_valid(self):
        _file = ROOT_DIR.joinpath('assets', 'banner.png')
        self.assertEqual(_file.exists(), True)
        self.assertNotEqual(get_file_size(_file), 0)

    def test_code_of_conduct_valid(self):
        _file = ROOT_DIR.joinpath('CODE_OF_CONDUCT.md')
        self.assertEqual(_file.exists(), True)
        self.assertNotEqual(get_file_size(_file), 0)

    def test_pull_request_template_valid(self):
        _file = ROOT_DIR.joinpath('.github', 'PULL_REQUEST_TEMPLATE')
        self.assertEqual(_file.exists(), True)
        self.assertNotEqual(get_file_size(_file), 0)

    def test_funding_valid(self):
        _file = ROOT_DIR.joinpath('.github', 'FUNDING.yml')
        self.assertEqual(_file.exists(), True)
        self.assertNotEqual(get_file_size(_file), 0)

    def test_workflows_valid(self):
        _file = ROOT_DIR.joinpath('.github', 'workflows', 'run-pytest.yml')
        self.assertEqual(_file.exists(), True)
        self.assertNotEqual(get_file_size(_file), 0)

        _file = ROOT_DIR.joinpath('.github', 'workflows', 'wgv-pyinstaller.yml')
        self.assertEqual(_file.exists(), True)
        self.assertNotEqual(get_file_size(_file), 0)

    def test_issue_template_valid(self):
        _file = ROOT_DIR.joinpath('.github', 'ISSUE_TEMPLATE', 'bug_report.md')
        self.assertEqual(_file.exists(), True)
        self.assertNotEqual(get_file_size(_file), 0)

        _file = ROOT_DIR.joinpath('.github', 'ISSUE_TEMPLATE', 'feature_request.md')
        self.assertEqual(_file.exists(), True)
        self.assertNotEqual(get_file_size(_file), 0)


if __name__ == '__main__':
    unittest.main()
