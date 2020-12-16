# Contribution Guide

You could help on:
- [WGViewer issues](https://github.com/WarshipGirls/WGViewer/issues)
- [WGViewer-tools issues](https://github.com/WarshipGirls/WGViewer-tools/issues)
- Code in-line TODOs

## Start

To contribute code,

1. start a Python virtual environment
2. install required packages: `pip install -r requirements.txt`
3. make a [pull request](../../pulls) when your code is ready :)

## Coding Styles

- This project followed most PEP standards
- Use indentation = 4 spaces
- For pure natural language strings, use double-quote; otherwise (involves variables), use single-quote

## Version Naming

WGViewer uses [packaging.version](https://packaging.pypa.io/en/latest/version.html) to test version naming.

- `version` format = `major.minor.micro`
- Valid notations = {a, b, c, r, beta, dev, pre, post, rev}
- Valid notations can appear once and only once in either `minor` or `micro` for the version number to be valid.
- notations are dropped while reading `minor` or `micro` field
  
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

## Commit message conventions

Please follow the [semantic commit messages](https://gist.github.com/joshbuchea/6f47e86d2510bce28f8e7f42ae84c716):

- `feat`: (new feature for the user, not a new feature for build script)
- `fix`: (bug fix for the user, not a fix to a build script)
- `docs`: (changes to the documentation)
- `style`: (formatting, missing semi colons, etc; no production code change)
- `refactor`: (refactoring production code, eg. renaming a variable)
- `test`: (adding missing tests, refactoring tests; no production code change)
- `chore`: (updating grunt tasks etc; no production code change)

## Packing into executable

To build executable on Windows OS, run

> win_build.bat

To build application on Linux OS, run

> ./linux_build.sh


