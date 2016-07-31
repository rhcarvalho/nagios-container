# RHMAP Nagios for Docker

[![Build Status](https://travis-ci.org/feedhenry/nagios-container.svg?branch=master)](https://travis-ci.org/feedhenry/nagios-container)

Nagios server in a Docker container for RHMAP.

## Development

### Running tests

```
python -m unittest discover -s plugins/default
```

### Style Guide and common problems

We use tools to enforce the [PEP8](https://www.python.org/dev/peps/pep-0008/)
style guide and prevent common problems on all Python code in this repository.

When developing the project, you'll need to install the dependencies:

```
pip install flake8 autopep8
```

Use [flake8](https://pypi.python.org/pypi/flake8) to verify that the code
conforms to the style guide, and is free of common errors:

```
flake8 --show-source
```

Automatically format source code using
[autopep8](https://pypi.python.org/pypi/autopep8):

```
find . -name '*.py' -print0 | xargs -0 autopep8 --in-place --aggressive --aggressive
```

You may integrate `flake8` and `autopep8` with your code editor.
