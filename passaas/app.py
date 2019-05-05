import connexion
import logging

from passaas.config import ProdConfig


def create_app(config_object=ProdConfig):
    logging.basicConfig(level=logging.DEBUG)

    app = connexion.App(__name__, specification_dir=config_object.APP_DIR)
    app.app.config.root_path = app.app.instance_path
    # app.app.json_encoder = encoder.JSONEncoder

    # Configuration from config.py
    app.app.config.from_object(config_object)

    # Ignore any configuration override in test configuration
    if app.app.config["ENV"] != "test":
        # Allow configuration override from the instance folder
        # http://flask.pocoo.org/docs/1.0/config/#instance-folders
        app.app.config.from_pyfile("config.cfg", silent=True)

    # strict_validation means that unexpected query parameters will return 400
    app.add_api("swagger.yml", strict_validation=True)

    register_extensions(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)

    return app


def register_extensions(app):
    pass


def register_errorhandlers(app):
    pass


def register_shellcontext(app):
    pass


def register_commands(app):
    pass
