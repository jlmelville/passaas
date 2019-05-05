# Password as a Service

[![AppVeyor Build Status](https://ci.appveyor.com/api/projects/status/github/jlmelville/passaas?branch=master&svg=true)](https://ci.appveyor.com/project/jlmelville/passaas)
[![Build Status](https://dev.azure.com/jlmelville/Python%20Pipeline/_apis/build/status/jlmelville.passaas?branchName=master)](https://dev.azure.com/jlmelville/Python%20Pipeline/_build/latest?definitionId=3&branchName=master)
[![Travis Build Status](https://travis-ci.org/jlmelville/passaas.svg?branch=master)](https://travis-ci.org/jlmelville/passaas)
[![Test Coverage Status](https://coveralls.io/repos/github/jlmelville/passaas/badge.svg)](https://coveralls.io/github/jlmelville/passaas)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/jlmelville/passaas.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/jlmelville/passaas/context:python)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/jlmelville/passaas.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/jlmelville/passaas/alerts/)

A REST service that provides a (read-only) REST interface to `passwd` and `group` files. Built
using [connexion](https://github.com/zalando/connexion).

## Prerequisites

Python 3.6 or higher.

## Installing

Install the requirements:

```bash
pip install -r requirements.txt
```

To install as a package:

```bash
pip install .
```

But you can run the app (see below) without installing, so that's probably not necessary. Just
run commands from the project root directory (i.e. the directory this README is in). The only
difference is where you put any extra configuration files -- see the
[Instance folder](https://github.com/jlmelville/passaas#instance-folder) section below.

## Running

Using Flask's built-in server:

```bash
python app.py
```

This will launch the app at `localhost:5000`.

To override the host and port, use the `--host` and `--port` arguments respectively, e.g.:

```bash
# listen on all assigned IPs on port 8080
python app.py --host=0.0.0.0 --port=8080
```

## API Documentation

Assuming the default host and port, the [OpenAPI](https://www.openapis.org/) documentation for the
API can be found at:

```bash
http://localhost:5000/api/ui/
```

## Configuration: specifying the `passwd` and `group` file

By default the `passwd` file is assumed to be at `/etc/passwd`, and the `group` file at
`/etc/group`. To use different locations, you have a couple of options:

### Instance folder

This is a standard Flask practice, so should be preferred. Place a `config.cfg` file in the
[instance folder](http://flask.pocoo.org/docs/1.0/config/#instance-folders) of the app, which, if
you are running the server without having installed passaas as a package, is probably a directory
called `instance` in the directory of the README you are reading now, i.e.:

```none
/README.md
/instance
    /config.cfg
```

If you *did* install passaas as a package, then it should be placed in the folder
`$PREFIX/var/passaas.app-instance`. You can find out `$PREFIX` from `sys.prefix`. For example, if
you have used [venv](https://docs.python.org/3/library/venv.html) to create a virtual environment
called `venv` (as is widely recommended), then `sys.prefix` will point to the folder `venv` where
you created the virtual environment and the instance folder is `venv/var/passaas.app-instance`.

Note that the exact name of the instance folder in the installed-package case differs a bit from
that given in the flask documentation, presumably because of how we get to the flask app underlying
the connexion app itself.

The content of the `config.cfg` should specify `PASSWD_PATH` and `GROUP_PATH` as absolute paths,
e.g.:

```python
PASSWD_PATH = "/abs/path/to/passwd"
GROUP_PATH = "/abs/path/to/group"
```

### Command line arguments

Alternatively, you can use the `--passwd` and `--group` options when lauching the server:

```bash
python app.py --passwd=/path/to/some/other/passwd --group=/path/to/some/other/group
```

If for some reason you like to really complicate life for yourself and you use an instance folder
*and* provide command-line options, be aware that the instance folder configuration overrides any
command-line option provided.

## Tests

To run the unit tests:

```shell
pip install -r test-requirements.txt
python setup.py test
```

## Deployment

See the `app_wsgi.py` file for something that can be used as a WSGI module with
[uwsgi](http://projects.unbit.it/uwsgi/). To deploy on port 8080 with 2 workers:

```bash
uwsgi --http :8080 --wsgi app_wsgi --processes 2
```

There are also command line options to override the default `passwd` and `group` locations: add the
arguments `--set passwd=/path/to/passwd` and `--set group=/path/to/group` to the above invocation.
The instance folder approach works unchanged.

## See Also

Examples of using connexion with unit testing are incredibly thin on the ground.
<https://github.com/hirose31/connexion-tiny-petstore> was invaluable in getting going. Also
[pytest-azurepipelines](https://pypi.org/project/pytest-azurepipelines/) made publishing test
results on Azure pipelines very easy.

## License

[The MIT License](https://opensource.org/licenses/MIT).
