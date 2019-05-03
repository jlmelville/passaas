from flask.helpers import get_debug_flag

from passaas.app import create_app
from passaas.config import ProdConfig, DevConfig

CONFIG = DevConfig if get_debug_flag() else ProdConfig

app = create_app(CONFIG)
app.run(port=CONFIG.APP_PORT, debug=CONFIG.DEBUG)
