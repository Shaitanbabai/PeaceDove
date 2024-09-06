from flask import Blueprint, jsonify, request
from helpers import validate_json, authenticated_route
import requests

# Создаем Blueprint для маршрутов, связанных с управлением дронами
drone_routes = Blueprint('drone_routes', __name__)

# Хранилище информации о дронах
drones = {}

@drone_routes.route("/drones", methods=["GET"])
@authenticated_route
def get_drones():
    """Возвращает список всех зарегистрированных дронов.

    Returns:
        Response: JSON-ответ с информацией о всех дронах и HTTP статус 200.
    """
    return jsonify(drones), 200

@drone_routes.route("/drones/<drone_id>", methods=["GET"])
@authenticated_route
def get_drone(drone_id):
    """Возвращает информацию о конкретном дроне по его идентификатору.

    Args:
        drone_id (str): Идентификатор дрона.

    Returns:
        Response: JSON-ответ с информацией о дроне и HTTP статус 200,
                  или сообщение об ошибке и HTTP статус 404, если дрон не найден.
    """
    drone = drones.get(drone_id)
    if drone:
        return jsonify(drone), 200
    return jsonify({"error": "Дрон не найден"}), 404

@drone_routes.route("/drones", methods=["POST"])
@validate_json
def create_drone():
    """Создает новый дрон на основе данных из запроса.

    Returns:
        Response: JSON-ответ с сообщением об успешном создании дрона и HTTP статус 201,
                  или сообщение об ошибке и HTTP статус 404, если не передан идентификатор дрона.
    """
    drone_id = request.json.get("drone_id")
    if drone_id:
        drones[drone_id] = request.json
        return jsonify({"message": f"Дрон {drone_id} добавлен"}), 201
    return jsonify({"error": "Не передан id дрона"}), 404

@drone_routes.route("/drones/<drone_id>/takeoff", methods=["POST"])
@authenticated_route
@validate_json
def takeoff_drone(drone_id):
    """Команда для взлета дрона.

    Args:
        drone_id (str): Идентификатор дрона.

    Returns:
        Response: JSON-ответ с сообщением об успешном взлете и HTTP статус 200,
                  или сообщение об ошибке и HTTP статус 404, если дрон не зарегистрирован,
                  или HTTP статус 500, если взлет завершился неудачно.
    """
    if drone_id not in drones:
        return jsonify({"error": f"Дрон c id: {drone_id} не зарегистрирован"}), 404
    altitude = request.json.get("altitude")
    drone_info = drones[drone_id]
    drone_url = drone_info.get("control_url") + "/takeoff"
    response = requests.post(drone_url, json={"altitude": altitude})
    if response.status_code == 200:
        return jsonify({"message": response.json().get("message")}), 200
    return jsonify({"error": f"Ошибка взлета дрона id: {drone_id}"}), 500