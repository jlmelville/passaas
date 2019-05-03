# Password as a Service

[![AppVeyor Build Status](https://ci.appveyor.com/api/projects/status/github/jlmelville/passaas?branch=master&svg=true)](https://ci.appveyor.com/project/jlmelville/passaas)
[![Build Status](https://dev.azure.com/jlmelville/Python%20Pipeline/_apis/build/status/jlmelville.passaas?branchName=master)](https://dev.azure.com/jlmelville/Python%20Pipeline/_build/latest?definitionId=3&branchName=master)
[![Travis Build Status](https://travis-ci.org/jlmelville/passaas.svg?branch=master)](https://travis-ci.org/jlmelville/passaas)
[![Test Coverage Status](https://coveralls.io/repos/github/jlmelville/passaas/badge.svg)](https://coveralls.io/github/jlmelville/passaas)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/jlmelville/passaas.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/jlmelville/passaas/context:python)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/jlmelville/passaas.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/jlmelville/passaas/alerts/)

A REST service built using [connexion](https://github.com/zalando/connexion).

## Installing

```bash
pip install -r requirements.txt
```

## Running

Using Flask's built-in server:

```bash
python app.py
```

This will launch the app at `localhost:9090`.

To override the host and port:

```bash
# listen at 127.0.0.1:5000
python app.py --host=127.0.0.1 --port=5000
```

### Specifying the `passwd` file

By default the `passwd` file is looked for at `/etc/passwd`. To use a different file, use the `--passwd` option:

```bash
python app.py --passwd=/path/to/some/other/passwd
```

## Documentation

Assuming the default host and port, the Swagger documentation for the API can be found at:

```bash
http://localhost:9090/api/ui/
```

## Tests

To run the unit  tests:

```shell
pip install -r test-requirements.txt
python setup.py test
```

## See Also

Examples of using connexion with unit testing are incredibly thin on the ground. <https://github.com/hirose31/connexion-tiny-petstore> was invaluable in getting going. Also [pytest-azurepipelines](https://pypi.org/project/pytest-azurepipelines/) made publishing test results on Azure pipelines very easy.

## License

[The MIT License](https://opensource.org/licenses/MIT).
