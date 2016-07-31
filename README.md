# RHMAP Nagios for Docker

[![Build Status](https://travis-ci.org/feedhenry/nagios-container.svg?branch=master)](https://travis-ci.org/feedhenry/nagios-container)

Nagios server in a Docker container for RHMAP.

## Development

Install dependencies:
```
pip install pep8
pip install autopep8
```

Run tests:

```
python -m unittest discover -s plugins/default
```

Style Guide:

All python modules should conform to the PEP8 style guide https://www.python.org/dev/peps/pep-0008/

To verify:

```
pep8 plugins/ --show-source
```

More info https://pypi.python.org/pypi/pep8

To format code:

```
autopep8 --in-place --aggressive --aggressive plugins/default/**/*.py
```

More info https://pypi.python.org/pypi/autopep8