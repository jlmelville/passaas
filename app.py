# pylint: disable=invalid-name
"""
Start web service on Flask server.

Run using:

python app.py

to start on localhost:5000

Host and port can be specified:

python app.py --host=0.0.0.0 --port=8080

Also the passwd and group file:

python app.py --passwd=/path/to/some/other/passwd --group=/path/to/some/other/group
"""
import argparse

from flask.helpers import get_debug_flag

from passaas.app import create_app
from passaas.config import ProdConfig, DevConfig

config = DevConfig if get_debug_flag() else ProdConfig

DEFAULT_HOST = "localhost"

parser = argparse.ArgumentParser(description="Start the Flask server.")
parser.add_argument(
    "-H",
    "--host",
    help="Hostname of the Flask app [default %s]" % DEFAULT_HOST,
    default=DEFAULT_HOST,
)
parser.add_argument(
    "-P",
    "--port",
    help="Port for the Flask app [default %d]" % config.APP_PORT,
    default=config.APP_PORT,
)
parser.add_argument(
    "-p",
    "--passwd",
    help="Path to passwd file [default %s]" % config.PASSWD_PATH,
    default=config.PASSWD_PATH,
)
parser.add_argument(
    "-g",
    "--group",
    help="Path to group file [default %s]" % config.GROUP_PATH,
    default=config.GROUP_PATH,
)
args = parser.parse_args()

config.APP_PORT = int(args.port)
config.PASSWD_PATH = args.passwd
config.GROUP_PATH = args.group

app = create_app(config)
app.run(host=args.host, port=config.APP_PORT, debug=config.DEBUG)
