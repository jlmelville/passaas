import os


class Config:
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    DEBUG = False
    TESTING = False
    APP_PORT = 9090
    PROPAGATE_EXCEPTIONS = False  # don't show traceback even if in debug mode
    PASSWD_PATH = "/etc/passwd"
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
