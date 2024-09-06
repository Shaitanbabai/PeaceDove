from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import jwt_required

def validate_json(f):
    """Декоратор для проверки, что запрос содержит данные в формате JSON.

    Этот декоратор проверяет, что входящий запрос имеет содержимое в формате JSON.
    Если это не так, возвращается ошибка 400 с описательным сообщением.

    Аргументы:
        f (function): Функция, которую необходимо декорировать.

    Возвращает:
        function: Декорированная функция, включающая проверку JSON.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            return jsonify({"error": "Запрос должен быть в формате JSON"}), 400
        return f(*args, **kwargs)
    return decorated_function

def authenticated_route(f):
    """Декоратор для обеспечения JWT-аутентификации на маршруте.

    Этот декоратор применяет JWT-аутентификацию к оборачиваемой функции,
    гарантируя, что пользователь аутентифицирован перед доступом к маршруту.

    Аргументы:
        f (function): Функция, которую необходимо декорировать.

    Возвращает:
        function: Декорированная функция, требующая JWT-аутентификацию.
    """
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        return f(*args, **kwargs)
    return decorated_function
