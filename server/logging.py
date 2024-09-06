import logging

def setup_logging():
    """
    Настройка логирования.
    """
    logging.basicConfig(level=logging.INFO)
    log_handler = logging.getLogger('drone_app')
    return log_handler

logger = setup_logging()
