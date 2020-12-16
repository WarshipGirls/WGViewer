# WGViewer Tests

To run tests, use

> # Start a virtual python environment, and install required packages  
> pytest test_file.py   # for testing single test file  
> pytest tests          # for testing all tests


- New features should come with corresponding tests

## Naming

Verify following; otherwise test files may not run.

- Verify that all files with test cases start with 'test_' word.
- Verify that all test cases names also start with 'test_' word.
- Verify that all test classes start with 'Test'
- Verify that `pytest.ini` file is created in the root directory
- Verify that `__init__.py` file exists in all directories/sub-directories of the project
