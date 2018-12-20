Hacking
=======

**TL;DR;** `poetry install`

To start hacking, please ensure you have a recent version of python installed.
You can use [`pyenv`](https://github.com/pyenv/pyenv) to easily switch between
python versions.

```
curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
pyenv install 3.6.6
pyenv local 3.6.6
```


Please install [`poetry`](https://github.com/sdispater/poetry). This is an
alternative to `pip` or `pipenv`.

```
pip install --user poetry
```

With this setup, you can run the following to setup the project dependencies
and run basic tests.

```
poetry install
poetry run python -m pytest
```
