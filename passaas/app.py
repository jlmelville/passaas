import connexion
import logging

from passaas.config import ProdConfig


def create_app(config_object=ProdConfig):
    logging.basicConfig(level=logging.DEBUG)

    app = connexion.App(__name__, specification_dir=config_object.APP_DIR)
    app.app.config.root_path = app.app.instance_path

    # Configuration from config.py
    app.app.config.from_object(config_object)

    # Ignore any configuration override in test configuration
    if app.app.config["ENV"] != "test":
        # Allow configuration override from the instance folder
        # http://flask.pocoo.org/docs/1.0/config/#instance-folders
        app.app.config.from_pyfile("config.cfg", silent=True)

    # strict_validation means that unexpected query parameters will return 400
    app.add_api("swagger.yml", strict_validation=True)

    return app
