import logging
import logging.config

def setup_logging(
    default_level=logging.INFO,
    log_file='app.log',
    log_format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'):
    """
    Настройка конфигурации логирования.

    Args:
        default_level (int): Уровень логирования по умолчанию. Использует значения из модуля logging, такие как logging.INFO.
        log_file (str): Имя файла, в который будет записываться лог.
        log_format (str): Формат строки логирования.
    """
    logging_config = {
        'version': 1,
        'formatters': {
            'default': {
                'format': log_format,
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'default',
                'level': default_level,
            },
            'file': {
                'class': 'logging.FileHandler',
                'filename': log_file,
                'formatter': 'default',
                'level': default_level,
            },
        },
        'root': {
            'handlers': ['console', 'file'],
            'level': default_level,
        },
    }

    # Применение конфигурации логирования из словаря.
    logging.config.dictConfig(logging_config)

# Пример использования
if __name__ == '__main__':
    setup_logging()  # Настройка логирования с параметрами по умолчанию.
    logger = logging.getLogger(__name__)  # Получение логгера для текущего модуля.
    logger.info("Logger is set up and ready to use!")  # Запись информационного сообщения в лог.
