from config import settings
from config.log import setup_logging
from backend.app import initialize_app
setup_logging()
application = initialize_app(settings)
