# Contribution Guide

- [WGViewer issue page](https://github.com/WarshipGirls/WGViewer/issues)
- [WGViewer-tools issue page](https://github.com/WarshipGirls/WGViewer-tools/issues)

## Start

To contribute code,

1. start a Python virtual environment
2. install required packages: `pip install -r requirements.txt`
3. make a [pull request](../../pulls) when your code is ready :)

### Packing into executable

To build executable on Windows OS, run

> win_build.bat

To build executable on Unix OS, update `fix_pyinstaller.py` with your directory location, run

> python tools/fix_pyinstaller.py > gui_main.spec  
> pyinstaller --clean gui_main.spec


## Version Naming

WGViewer uses [packaging.version](https://packaging.pypa.io/en/latest/version.html) to test version naming.

- `version` format = `major.minor.micro`
- Valid notations = {a, b, c, r, beta, dev, pre, post, rev}
- Valid notations can appear once and only once in either `minor` or `micro` for the version number to be valid.
- notations are dropped when reading `minor` or `micro` field
  
Some valid example:
``` 
0.0.1
0.0.1a
0.0.1beta
0.0.beta1   # valid but WGViewer does not recommend you to use
0.dev.1
```

The order of the version notation is:

```
(any int) > rev > r > post > c = pre > beta > b > a > dev
```


## Branch Naming

A branch name consists of a version number and the branch's responsibility (be specific and focused). For example:

```
v0.1.0-side-dock
v0.1.1dev-docs
```

## Coding Styles

- This project followed most PEP standards
- Use indentation = 4 spaces
- For pure natural language strings, use double-quote; otherwise (involves variables), use single-quote
