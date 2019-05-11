# Project Structure

Some brief notes on the project structure for non-Flask experts.

The app itself lives under:

## `passaas`

If you've ever looked at an MVC-framework in the style of Rails, then there shouldn't be anything
too confusing going on. The good news is there is nothing database-related *or* view-related,
which hugely cuts down on the number of files to wade through.

You have immense freedom do whatever you want with Flask. I split the code into models and
controllers because for most real services, you are going to want do some sort of organization
in this style.

### `models`

These files contain a representation of the "domain" (such that it is in this app), i.e.
Groups and Users, as well as code to read them in from storage. Normally, you would be dealing with
database code here, but we just read from some text files (i.e. `/etc/group` and `/etc/passwd`).

The Groups and Users are defined as
[named tuples](https://docs.python.org/3.7/library/collections.html#collections.namedtuple), not
because they need to be, but because I found it convenient: they are immutable, which because
this service is read-only is ideal. I also used the `typing` module to make it clear what the type
of each entry in the tuple was supposed to be. There were two downsides to this: first, the
combination of the `typing` module with named tuples meant that this app is incompatible with
Python 3.5, and second, Flask doesn't know how to convert named tuples to JSON output (more on that
in the `controllers` section). An alternative to named tuples are
[data classes](https://docs.python.org/3/library/dataclasses.html), but they are mutable and they
restrict you even further to Python 3.7 (or presumably later versions).

In short, you don't need to use named tuples at all. Plain old classes are fine.

### `controllers`

The functions in these files are referenced in `openapi.yml`. It is
the magic of connexion that it knows how to take what's in `openapi.yml` and route a request
like `GET /api/users/1` to the right function. The controller then uses some functions in the
models to get the data it needs, in the form of the object provided by the `models`. When we
return these results, they should get converted to the output format (also specified in
`openapi.yml`), which in this app is JSON.

As mentioned above, my decision to use named tuples as my models ran into a slight problem,
as connexion (or rather Flask at this part of the code) doesn't know how to automatically convert
these to JSON. The answer was to convert them to dictionaries before returning them from the
controller functions: named tuples have a method to do just that.

The resulting function is in `util.py`. But to be clear, if I had used a less exotic technique for
my models, this would have been handled for me. So you probably won't need that function or that
entire file.

### `config.py`

The configurations for production, development and testing. Usually this is full of
database-related configuration, but there's much less going on here. Notably, this sort of file is
entirely absent from most other connexion apps (except the mighty `connexion-tiny-petstore`, of
course), but is exactly what is needed for testing purposes, and for `passaas`, a place to specify
a non-default location for input files (which we can use in turn to test unhappy path code like a
missing or incorrectly formatted file).

### `app.py`

This is what flask calls the application factory. This is where you fetch configuration from various
places and then instantiate a Flask application. Plenty of flask material cover things you might
want to do at this point.

But because we are using connexion, the app we create is actually a completely different object
from the flask app. You can't configure it using any of the information provided by flask
tutorials. Fortunately, you can get to the underlying flask app, which is stored as the `app`
attribute of the connexion app. Unfortunately, the connexion app also tends to be called `app`,
leading to code that is mainly configuration, but partly uses `app`, and some of which uses
`app.app`.

To avoid confusion, I use `conn_app` and `flask_app` as variable names in this file, to try and
make it easier to see which bits are connexion configuration, and which bits are handled by flask.
Once you have that clear in your mind, it's easy to go back to flask documentation and know that it
all should apply to `flask_app`.

As a further point of confusion, in most connexion examples, the work done in this file is combined
with the code to start up the flask server if it's run as a script, and the entire file would
normally live in the root of the project. The
[connexion-tiny-petstore](https://github.com/hirose31/connexion-tiny-petstore/) keeps both files,
but they are both named `app.py` in that project which I find way too confusing. I have renamed
the flask server startup script to `server.py` (see below).

This file also contains code to support using the
[instance folder](http://flask.pocoo.org/docs/1.0/config/#instance-folders) to allow overriding
the configuration. This seems like the preferred way to do this sort of customization with a flask
app, rather than using environment variables.

### `tests`

This directory is where the tests live. These are all
[WebTest](https://docs.pylonsproject.org/projects/webtest/en/latest/) tests, so they are closer
to functional tests rather than unit tests, but for a project this size, that wasn't an issue and
with a JSON-based output, it's not that painful.

#### `conftest.py`

This file is where the configuration of the test app is carried out. There's a three-stage process
involved. First, a new configuration class is created, then a fixture creates an app using that
configuration. In a final fixture WebTest wraps that app. Inside the test classes, you just use
that last fixture and start making requests and making assertions on the response.

I wanted to test multiple app configurations (including configurations that are broken in some
way), and because you have to generate a triplet of config and two fixtures for each app, it gets
quite verbose. Therefore, I stuck these extra configurations in their own submodules:

#### `bad_group_config` and `bad_passwd_config`

These submodules contain the configuration and fixtures for misconfigured servers. I put them in
their own submodules only because `conftest.py` was getting a bit big and overwhelming. To start
out, I recommend just putting everything into `conftest.py`.

## `setup.py`

This is a pretty standard `setup.py`, based on looking at the example in the
[PyPA sample project](https://github.com/pypa/sampleproject/blob/master/setup.py) and also running
[pyroma](https://github.com/regebro/pyroma) via the
[prospector](https://prospector.landscape.io/en/master/) tool until it stopped complaining.

In one extra piece of hackery
[to avoid having to define the version string in multiple places](https://packaging.python.org/guides/single-sourcing-package-version/),
I parse the `openapi.yaml` file. If you aren't creating a connexion app, you can just hardcode it here,
and the `__init__.py` of the package should still work to allow this sort of thing:

## `setup.cfg`

Contains configuration to make running tests and test coverage easier.

## `MANIFEST.in`

Needed only if you want or need to install the package (e.g. `pip install .` it), rather than just
run commands from the project root. For this app, the only extra non-python code that needs to be
present is the `openapi.yaml` file.

## `server.py`

This is a script that creates an instance of the app and starts up the flask server. You will be
warned not to run it in production. I've added some command line options so you can choose the
port and hostname to run under, which might be useful generically. There are also some extra options
to specify a non-default `group` and `passwd` file, but this isn't going to scale as your
configuration needs grow. The
[instance folder](http://flask.pocoo.org/docs/1.0/config/#instance-folders) approach is the better
way of doing things.

## `wsgi.py`

This WSGI-fies the app so it can be used with [uwsgi](http://projects.unbit.it/uwsgi/), which is
a more sensible deployment option than the flask server. Note that you can't install this on
Windows, but it *does* work with WSL. You don't need this, but like being able to `pip install` your
package, if you can deploy your app to uwsgi, that's a pretty good sign you have things working
right, so it's worth trying now and again.

## Tests and Coverage

Make sure you've installed the test dependencies:

```bash
pip install -r test-requirements.txt
```

To run the tests:

```bash
python setup.py test
```

To run test coverage:

```bash
coverage run setup.py test && coverage report
```
