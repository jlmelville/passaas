# pylint: disable=too-few-public-methods
"""
Connexion Configuration.

Rather than edit this file, you should prefer to add a config.cfg file to the instance
folder. See the project root folder server.py file for an example of how the config
file is used. The instance folder is located in one of two places:

* if you haven't pip installed this package:
    /instance
        config.cfg <--- your config file
    /passaas
        config.py <--- this file
* if you have installed this package (e.g. by "pip install ."):
    /$PREFIX
        /var
            /passaas.app-instance
                config.cfg <--- your config file
$PREFIX is whatever sys.prefix says it is. In a venv, it's /path/to/venv/var, so the
full path to your config.cfg would be /path/to/venv/var/passaas.app-instance/config.cfg

Some example config.cfg file entries are:

PASSWD_PATH = /abs/path/to/passwd
GROUP_PATH = /abs/path/to/group
"""
import os


class Config:
    """Generic configuration."""

    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    DEBUG = False
    TESTING = False
    APP_PORT = 5000
    PROPAGATE_EXCEPTIONS = False  # don't show traceback even if in debug mode
    PASSWD_PATH = "/etc/passwd"  # nosec
    GROUP_PATH = "/etc/group"


class ProdConfig(Config):
    """Production configuration."""

    ENV = "production"
    DEBUG = False


class DevConfig(Config):
    """Development configuration."""

    ENV = "development"
    DEBUG = True
    PROPAGATE_EXCEPTIONS = True


class TestConfig(Config):
    """Testing configuration."""

    ENV = "test"
    DEBUG = True
    TESTING = True
    PASSWD_PATH = os.path.abspath(
        os.path.join(Config.PROJECT_ROOT, "tests", "test_data", "passwd")
    )
    GROUP_PATH = os.path.abspath(
        os.path.join(Config.PROJECT_ROOT, "tests", "test_data", "group")
    )
