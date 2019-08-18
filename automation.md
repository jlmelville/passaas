# Automation Configuration

Here's a run-down of the files that are related to continuous integration and things of that nature.
If you don't care about these services, then these files can be safely removed without affecting the
running or installation of the app.

## Prerequisites

If you *do* want to use these services, note that you will need to register your github account
with them and give them access to your repo. It's all pretty painless, although in typical Microsoft
fashion, [azure pipelines](https://dev.azure.com) is a bit more work. You will need a Microsoft
account of some kind to log into it, although these are freely obtained.

## Continuous Integration

The continuous integration services attempt to install and run the tests for Python 3.6 and 3.7
on a variety of architectures.

### `ci`

The folder contains some bash scripts. These are only used by [travis-ci](https://travis-ci.org),
but not that Travis is where I run the coverage checks and upload code coverage to
[coveralls](coveralls.io).

### `.travis.yml`

The [travis-ci](https://travis-ci.org) configuration, which runs under Linux. As mentioned above,
this is the only CI that runs code coverage. It also runs the
[black code formatter](https://github.com/python/black) in "check" mode: if black wants to reformat
the code, this indicates that I forgot to run it before checking in the code and the build is
failed. This is a good way to enforce a fixed code layout.

### `appveyor.yml`

The [appveyor](https://ci.appveyor.com) configuration for running CI on Windows.

### `azure-pipelines.yml`

The [azure pipelines](https://dev.azure.com) configuration, which runs CI on Mac.

## Code Coverage

For code coverage, I use [coveralls](coveralls.io), uploading the result after a successful Travis
CI run. [codacy](https://codacy.com/) and [Code Climate](https://codeclimate.com) also offer code
coverage checking, but it's not as easy to set up as with coveralls.

## Code Quality

These services provide checks on the code quality, running linting software, checking complexity
and looking for duplication, security issues and so on. Some of them allow you to control their
reports with the same linting configuration files you use for running linters locally (see below
for more on that). It's definitely worth looking at their output, although I am also very happy
to ignore some of their advice. For example, [Code Climate](https://codeclimate.com) doesn't like
the number of parameters that are available for querying groups and users in their respective
controllers, but I can't think of a good way to avoid that.

Whatever configuration I did to [codacy](https://codacy.com/) and [LGTM](https://lgtm.com), I did
through their website rather than a configuration file.

### `codeclimate.yml`

Configuration for [Code Climate](https://codeclimate.com).

## Code Formatting

To enforce code formatting, I run the [black code formatter](https://github.com/python/black)
before running tests locally, e.g.:

```bash
black . && python setup.py test
```

You can create a git hook to run black before checking in, but I didn't have much luck with that
on Windows. An alternative that works just as well for VS Code is to set up `black` to autoformat
on save. For that, see the sample `settings.json` file below. As mentioned above, the Travis CI
will fail if it detects that black wasn't run on a checkin.

The way black formats code means that you will need to adjust some settings of some of the linting
tools, particularly `pylint` and `flake8`. Most pertinently, `black` tries to set line lengths to
88 characters, which differs from the defaults of `pylint` and `flake8`.

## Linters

Configuration for these all live in the `lint` subdirectory, as the associated configuration and
helper files were cluttering up the main directory.

### Quick installation

The linters can be installed with:

```bash
./install-linters.sh
```

This just uses `pip` to install them in a specific order (with some uninstalling), in order to get
up-to-date and compatible versions of the specific tools I have chosen (i.e. those which are
well-integrated with VS Code). You only have to do it once. It's easy enough to follow the
procedure on Windows manually.

To run the linters from the command-line you can use:

```bash
./check-file.sh <file>
```

But I use the integrated VS code support. See below for a `settings.json` that sets this up.

### Linting Details

Wow,
[Python has a lot of linting tools](https://github.com/vintasoftware/python-linters-and-code-analysis).
I have some suggestions about which ones to run, based on those that are integrated into the
Python extension of [Visual Studio Code](https://code.visualstudio.com), which means that their
opinions will appear in the 'Problems' tab, along with an icon indicating the severity of the issue.

I have configured the following tools as a good start for linting black-formatted code, trying
to avoid false positives and having multiple tools flag the same problem. I have erred on the
side of strictness, so you will definitely want to further tweak these settings to turn off
complaints that you won't have any plans to fix, particularly with regard to naming conventions.

### `.pylintrc`

This controls [pylint](https://www.pylint.org/). This has lots of opinions on everything, so you
will want to configure it. Fortunately, you can also turn off particular complaints over the
scope of an entire file via inline comments that begin `# pylint:`. This is useful in test code,
which often defy the basic norms of good taste for application code and so a smaller number of tests
are relevant in these files.

### `.flake8`

This controls [flake8](http://flake8.pycqa.org/en/latest/), which combines several linters in one:
[pycodestyle](https://pypi.org/project/pycodestyle/) (which used to be called `pep8`),
[pep8-naming](https://github.com/PyCQA/pep8-naming), [PyFlakes](https://github.com/PyCQA/pyflakes),
and [mccabe](https://github.com/PyCQA/mccabe). If you are beginning to get confused, don't worry,
it gets worse. The maintainer of `flake8` maintains `pycodestyle`, `pyflakes` and `mccabe`, so this
is probably as good a place as any to use these tools together.

### `bandit.yml`

This controls [bandit](https://github.com/PyCQA/bandit), which looks for security flaws.

### `.prospector.yaml`

Like `flake8`, [prospector](https://prospector.landscape.io/en/master/) collects a lot of other
tools. In fact, `prospector` uses everything `flake8` does and then some, including `pylint`. Sounds
perfect, so why use `flake8` and `pylint` separately? Two reasons: first, prospector uses older
versions of the tools and you can't just forcibly upgrade `pycodestyle` or `pylint` as this can
cause an error with `prospector`. Second, Visual Studio Code reports all of the output as errors,
with no gradation of warning or information to distinguish between something really bad like
a broken import versus something innocuous like a badly formatted docstring. Therefore, I prefer
to use `pylint` and `flake8` separately. In this project, I have only turned on the tools that
aren't integrated into other programs supported by Visual Studio, which in this case is
[dodgy](https://github.com/landscapeio/dodgy) (which looks for things like hard-coded passwords or
other credentials) and [pyroma](https://github.com/regebro/pyroma) (checks `setup.py`).

### `pydocstyle`

Finally, there's [pydocstyle](http://www.pydocstyle.org/en/3.0.0/usage.html), which checks for
the presence and quality of docstrings. Unless you are fastidious about separating your public
interface from the implementation, you can expect a lot of messages. In particular, you probably
don't want to point this at your test code. I think being reminded to add a docstring in each test
file about what that file is testing, and a docstring for each class is useful documentation. On
the other hand, you will also be asked to document each function, which is definitely overkill.
Rather than configure it to run all the time, I prefer to edit the
`"python.linting.pydocstyleEnabled"` entry in `.vscode/settings.json` from `false` to `true` when
it's time to look at documentation, and turn it off at other times.

### `settings.json`

A sample chunk of the Visual Studio Code `settings.json` using a virtual environment might look like:

```json
{
    "python.jediEnabled": false,
    "python.pythonPath": "venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.banditEnabled": true,
    "python.linting.banditArgs": [
        "-c",
        "lint/bandit.yml",
        "-q"
    ],
    "python.linting.flake8Enabled": true,
    "python.linting.flake8Args": [
        "--config",
        "lint/.flake8"
    ],
    "python.linting.mypyEnabled": false,
    "python.linting.pep8Path": "pycodestyle",
    "python.linting.pep8Enabled": false,
    "python.linting.prospectorEnabled": true,
    "python.linting.prospectorArgs": [
        "--profile",
        "lint/.prospector.yaml"
    ],
    "python.linting.pylamaEnabled": false,
    "python.linting.pylintEnabled": true,
    "python.linting.pylintArgs": [
        "--rcfile",
        "lint/.pylintrc"
    ],
    "python.linting.pylintUseMinimalCheckers": false,
    "python.linting.pylintCategorySeverity.refactor": "Information",
    "python.linting.maxNumberOfProblems": 1000,
    "python.linting.pydocstyleEnabled": false,
    "editor.rulers": [
        88
    ],
    "python.formatting.provider": "black",
    "python.formatting.blackPath": "venv/bin/black",
    "editor.formatOnSave": true
}
```

With anaconda on Windows, you probably need the first few entries to be along the lines of:

```json
    "python.jediEnabled": false,
    "python.condaPath": "C:\\path\\to\\Anaconda\\Scripts",
    "python.pythonPath": "C:\\path\\to\\Anaconda\\envs\\some-env\\python.exe",
```

This turns on the tools discussed above, and leaves others off, including
[pylama](https://github.com/klen/pylama), which I haven't discussed: it is a tool with a similar
set of linters to `prospector` and `flake8`. It also uses `black` to autoformat the code on save.
