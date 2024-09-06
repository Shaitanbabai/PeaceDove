import jwt
import logging
from functools import wraps

# Настройка логирования
logging.basicConfig(filename='security.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class SafetyCheck:
    def __init__(self, secret_key: str):
        self.__secret_key = secret_key

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = kwargs.get('token')
            try:
                if self.check_token(token):
                    return func(*args, **kwargs)
                else:
                    logging.warning("Команда отклонена: неверный токен")
                    return None
            except Exception as e:
                logging.error(f"Ошибка при выполнении команды: {e}")
                return None

        return wrapper

    def check_token(self, token):
        try:
            jwt.decode(token, self.__secret_key, algorithms=['HS256'])
            return True
        except jwt.InvalidTokenError as e:
            logging.warning("Ошибка декодирования токена: %s", e)
            return False