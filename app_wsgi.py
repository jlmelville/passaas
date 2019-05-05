# pylint: disable=invalid-name,import-error
# uwsgi isn't installable on Windows, so pylint will always complain about an import error
# this is just an example deployment file, you don't need to use it
"""
Example usage passing non-standard locations for passwd and group:
uwsgi --http :8080 --wsgi app_wsgi --processes 2 --set passwd=/tmp/passwd --set group=/tmp/group
"""

from flask.helpers import get_debug_flag

import uwsgi

from passaas.app import create_app
from passaas.config import ProdConfig, DevConfig

config = DevConfig if get_debug_flag() else ProdConfig

config.PASSWD_PATH = uwsgi.opt.get("passwd", config.PASSWD_PATH)
config.GROUP_PATH = uwsgi.opt.get("group", config.GROUP_PATH)

app = create_app(config)
application = app.app
