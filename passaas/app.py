"""The Connexion Application."""
import logging
import connexion

from passaas.config import ProdConfig


def create_app(config_object=ProdConfig):
    """
    Application factory for the connexion app.

    Application will be created with the specified configuration.
    """
    logging.basicConfig(level=logging.DEBUG)

    conn_app = connexion.App(__name__, specification_dir=config_object.APP_DIR)
    flask_app = conn_app.app

    # Seemed to need this to get the instance folder support working
    # https://github.com/zalando/connexion/issues/556
    flask_app.config.root_path = flask_app.instance_path
    # Configuration from config.py
    flask_app.config.from_object(config_object)

    # Ignore any configuration override in test configuration
    if flask_app.config["ENV"] != "test":
        # Allow configuration override from the instance folder
        # http://flask.pocoo.org/docs/1.0/config/#instance-folders
        flask_app.config.from_pyfile("config.cfg", silent=True)

    # strict_validation means that unexpected query parameters will return 400
    conn_app.add_api("openapi.yaml", strict_validation=True)

    return conn_app
