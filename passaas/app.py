import connexion
import logging

from passaas.config import ProdConfig


def create_app(config_object=ProdConfig):
    logging.basicConfig(level=logging.DEBUG)

    app = connexion.App(__name__, specification_dir=config_object.APP_DIR)
    # app.app.json_encoder = encoder.JSONEncoder
    app.app.config.from_object(config_object)
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
