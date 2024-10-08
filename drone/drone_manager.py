from abc import ABC, abstractmethod
import socket
import airsim
from pymavlink import mavutil
from mission_manager import MissionManager
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Создание экземпляра MissionManager
mission_manager = MissionManager()

# Симулированная база данных дронов
DRONE_DATABASE = [
    {"drone_id": "DJI001", "model": "Phantom 4", "manufacturer": "DJI", "sensors": ["Camera", "GPS", "Altimeter", "Anemometer"], "max_speed": 20, "max_altitude": 6000, "battery_capacity": 80},
    {"drone_id": "AIRSIM001", "model": "AirSim Model", "manufacturer": "AirSim", "sensors": ["Camera", "GPS", "Altimeter", "Anemometer"], "max_speed": 15, "max_altitude": 5000, "battery_capacity": 80},
    # Добавьте больше дронов при необходимости
]

class DroneFlyweight:
    def __init__(self, drone_id, model, manufacturer, sensors, max_speed, max_altitude, battery_capacity):
        """Инициализирует экземпляр DroneFlyweight.

        Args:
            drone_id (str): Идентификатор дрона.
            model (str): Модель дрона.
            manufacturer (str): Производитель дрона.
            sensors (list): Список сенсоров дрона.
            max_speed (int): Максимальная скорость дрона.
            max_altitude (int): Максимальная высота дрона.
            battery_capacity (int): Ёмкость батареи дрона.
        """
        self._drone_id = drone_id
        self._model = model
        self._manufacturer = manufacturer
        self._sensors = sensors
        self._max_speed = max_speed
        self._max_altitude = max_altitude
        self._battery_capacity = battery_capacity

    def operation(self, unique_state):
        """Выполняет операцию дрона с заданным уникальным состоянием.

                Args:
                    unique_state (dict): Уникальные параметры состояния, включая скорость, высоту и заряд батареи.
                """
        print(f"""
        ===============
        Drone
            Drone_ID: {self._drone_id}
            Model: {self._model}
            Manufacturer: {self._manufacturer}
            Sensors: {self._sensors}
            Max Speed: {self._max_speed}
            Max Altitude: {self._max_altitude}
            Battery Capacity: {self._battery_capacity}

        Current Parameters
            Speed: {unique_state["speed"]}
            Altitude: {unique_state["altitude"]}
            Battery: {unique_state["battery"]}
        """)

# Абстрактная фабрика для создания дронов
class DroneFactory(ABC):
    """Абстрактная фабрика для создания дронов.

    Attributes:
        _drones (dict): Словарь для хранения созданных дронов.
    """

    def __init__(self):
        """Инициализирует экземпляр DroneFactory."""
        self._drones = {}

    def get_drone(self, drone_id, model, manufacturer, sensors, max_speed, max_altitude, battery_capacity):
        """Возвращает экземпляр дрона из хранилища или создает новый, если он отсутствует.

        Args:
            drone_id (str): Идентификатор дрона.
            model (str): Модель дрона.
            manufacturer (str): Производитель дрона.
            sensors (list): Список сенсоров дрона.
            max_speed (int): Максимальная скорость дрона.
            max_altitude (int): Максимальная высота дрона.
            battery_capacity (int): Ёмкость батареи дрона.

        Returns:
            DroneFlyweight: Экземпляр дрона.
        """
        key = (drone_id, model, manufacturer, tuple(sensors), max_speed, max_altitude, battery_capacity)
        if key not in self._drones:
            self._drones[key] = self.create_drone(drone_id, model, manufacturer, sensors, max_speed, max_altitude, battery_capacity)
        return self._drones[key]

    @abstractmethod
    def create_drone(self, drone_id, model, manufacturer, sensors, max_speed, max_altitude, battery_capacity):
        pass

# Конкретная фабрика для дронов DJI
class DJIDroneFactory(DroneFactory):
    def create_drone(self, drone_id, model, manufacturer, sensors, max_speed, max_altitude, battery_capacity):
        return DroneFlyweight(drone_id, model, manufacturer, sensors, max_speed, max_altitude, battery_capacity)

# Конкретная фабрика для дронов AirSim
class AirSimDroneFactory(DroneFactory):
    def create_drone(self, drone_id, model, manufacturer, sensors, max_speed, max_altitude, battery_capacity):
        return DroneFlyweight(drone_id, model, manufacturer, sensors, max_speed, max_altitude, battery_capacity)


# Абстрактный интерфейс для API управления дроном
class IDroneAPI(ABC):
    """
    Attributes:
        client: Клиент для подключения к дрону.
        connect_uri (str): URI для подключения.
    """

    def __init__(self, connect_uri=None):
        """Инициализирует экземпляр IDroneAPI.

        Args:
            connect_uri (str, optional): URI для подключения. По умолчанию None.
        """
        self.client = None
        self.connect_uri = connect_uri

    @abstractmethod
    def connect(self):
        """Подключается к дрону."""
        pass

    @abstractmethod
    def send_command(self, command):
        """Отправляет команду дрону.

        Args:
            command (str): Команда для отправки.
        """
        pass


# Класс API для работы с AirSim
class AirSimAPI(IDroneAPI):
    def connect(self):
        """Подключается к AirSim."""
        self.client = airsim.MultirotorClient()
        try:
            self.client.confirmConnection()
            logger.info("Подключение через AirSim успешно")
        except Exception as e:
            logger.error(f"Ошибка подключения через AirSim: {e}")
            raise

    def send_command(self, command):
        logger.info(f"AirSim оправлена команда: {command}")

# Класс API для работы с MAVLink
class DJIDroneAPI(IDroneAPI):
    def connect(self):
        """Подключается к дрону DJI по заданному URI.
        """
        logger.debug(f"Попытка подключения к {self.connect_uri}")
        try:
            self.client = mavutil.mavlink_connection(self.connect_uri)
            self.client.wait_heartbeat()
            logger.info("Соединение с дроном DJI установлено")
        except socket.gaierror as e:
            logger.error(f"Ошибка получения адреса: {self.connect_uri} - {e}")
            raise
        except Exception as e:
            logger.error(f"Неожиданная ошибка: {e}")
            raise

    def send_command(self, command):
        logger.info(f"DJI отправлена команда: {command}")


# Фабрика для создания объектов API для дронов
class DroneAPIFactory:
    @staticmethod
    def get_drone_api(manufacturer, connect_uri):
        """Возвращает экземпляр соответствующего API в зависимости от заданного производителя.

        Args:
            manufacturer (str): Название производителя дрона.
            connect_uri (str): URI для подключения к дрону.

        Returns:
            IDroneAPI: Экземпляр API для работы с дроном.
        """
        if manufacturer.lower() == "dji":
            return DJIDroneAPI(connect_uri)
        else:
            return AirSimAPI()

# Класс для логирования действий с дронами
class DroneLogger:
    def log_approval(self, drone_id, parameters):
        """Логирует одобрение дрона для выполнения миссии.

        Args:
            drone_id (str): Идентификатор дрона.
            parameters (dict): Параметры дрона.
        """
        logger.info(f"Drone ID {drone_id} approved with parameters: {parameters}")

    def log_selection(self, drone_id):
        """
        Логирует выбор дрона для выполнения миссии.
        """
        logger.info(f"Drone {drone_id} selected for mission.")

def select_drone_for_mission(required_battery_capacity):
    """Выбирает дроны для миссии на основе емкости батареи.

        Args:
            required_battery_capacity (int): Требуемая емкость батареи.

        Returns:
            list: Список идентификаторов одобренных дронов.
        """
    approved_drones = []
    for drone_data in DRONE_DATABASE:
        if drone_data["battery_capacity"] >= required_battery_capacity:
            logger.info(f"Drone {drone_data['drone_id']} meets the battery capacity requirement.")
            approved_drones.append(drone_data["drone_id"])
        else:
            logger.warning(f"Drone {drone_data['drone_id']} does not meet the battery capacity requirement.")
    return approved_drones

def approve_drone_for_mission(drone_id):
    """Допускает дрон к миссии по его идентификатору.
    Returns:
        dict or None: Информация о дроне, если одобрен, иначе None.
    """
    drone_data = next((d for d in DRONE_DATABASE if d["drone_id"] == drone_id), None)

    if drone_data is None:
        logger.warning(f"Drone ID {drone_id} not found in DRONE_DATABASE.")
        return None

    parameters = {
        "manufacturer": drone_data.get("manufacturer"),
        "status": drone_data.get("status", "operational"),
        "battery_capacity": drone_data.get("battery_capacity")
    }

    if not check_manufacturer_api(parameters['manufacturer']):
        logger.error(f"Drone {drone_id} not approved. Manufacturer API check failed.")
        return None

    if parameters['status'] != "operational":
        logger.warning(f"Drone ID {drone_id} is not operational.")
        return None

    drone_logger.log_approval(drone_id, parameters)

    return {"drone_id": drone_id, "parameters": parameters}


def check_manufacturer_api(manufacturer):
    """Проверяет поддержку API для указанного производителя.
    Returns:
        bool: True, если производитель поддерживается, иначе False.
    """
    api_object = DroneAPIFactory.get_drone_api(manufacturer, "dummy_connect_uri")
    if api_object is not None:
        logger.info(f"Manufacturer {manufacturer} is supported.")
        return True
    else:
        logger.warning(f"Manufacturer {manufacturer} is not supported.")
        return False

def send_validated_drones_to_mission_manager(valid_drones):
    """Передаёт список валидных дронов в модуль менеджера миссий.

        Args:
            valid_drones (list): Список идентификаторов валидных дронов.
        """
    try:
        mission_manager.receive_validated_drones(valid_drones)
        logger.info(f"Validated drones sent to mission manager: {valid_drones}")
    except AttributeError:
        logger.error("Нет подключения к mission_manager.py, назначение дронов на миссии невозможно. "
                     "Реализуйте receive_validated_drones в коде mission_manager.py")

# Пример использования
if __name__ == "__main__":
    # Создаем объект класса DroneLogger
    drone_logger = DroneLogger()

    # Выбор дронов, удовлетворяющих требованиям к емкости батареи
    selected_drones = select_drone_for_mission(75)

    # Список валидных дронов для передачи в менеджер миссий
    validated_drones = []

    # Проверка и допуск дронов к миссии
    for drone_id in selected_drones:
        approved_drone = approve_drone_for_mission(drone_id)
        if approved_drone:
            drone_logger.log_selection(approved_drone['drone_id'])
            logger.info(f"Drone ID {approved_drone['drone_id']} is approved for flight and mission.")
            validated_drones.append(approved_drone)

    # Передача валидированных дронов в менеджер миссий
    send_validated_drones_to_mission_manager(validated_drones)