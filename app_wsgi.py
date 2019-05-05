"""
Example usage passing non-standard locations for passwd and group:
uwsgi --http :8080 --wsgi app_wsgi --processes 2 --set passwd=/tmp/passwd --set group=/tmp/group
"""

import uwsgi

from flask.helpers import get_debug_flag

from passaas.app import create_app
from passaas.config import ProdConfig, DevConfig

config = DevConfig if get_debug_flag() else ProdConfig

config.PASSWD_PATH = uwsgi.opt.get("passwd", config.PASSWD_PATH)
config.GROUP_PATH = uwsgi.opt.get("group", config.GROUP_PATH)

app = create_app(config)
application = app.app
