from abc import ABC, abstractmethod


class Sensor(ABC):
    """
    Абстрактный класс для сенсора.
    """

    @abstractmethod
    def read_data(self):
        pass


class Altimeter(Sensor):
    """
    Класс для работы с альтиметром.
    """

    def __init__(self):
        self.altitude = 0

    def read_data(self):
        # Пример чтения данных с альтиметра
        # В реальной реализации здесь будет код для взаимодействия с устройством
        self.altitude = self._get_altitude_from_device()
        return self.altitude

    def _get_altitude_from_device(self):
        # Заглушка для получения данных с устройства
        # В реальной реализации здесь будет код для взаимодействия с устройством
        return 100  # Примерное значение высоты


class GPSSensor(Sensor):
    """
    Класс для работы с GPS датчиком.
    """

    def __init__(self):
        self.latitude = 0.0
        self.longitude = 0.0

    def read_data(self):
        # Пример чтения данных с GPS
        # В реальной реализации здесь будет код для взаимодействия с устройством
        self.latitude, self.longitude = self._get_gps_data_from_device()
        return {'latitude': self.latitude, 'longitude': self.longitude}

    def _get_gps_data_from_device(self):
        # Заглушка для получения данных с устройства
        # В реальной реализации здесь будет код для взаимодействия с устройством
        return 55.7558, 37.6176  # Примерные координаты (Москва)


class SensorManager:
    """
    Класс для управления сенсорами.
    """

    def __init__(self):
        self.sensors = []
        self.observers = []

    def add_sensor(self, sensor):
        self.sensors.append(sensor)

    def remove_sensor(self, sensor):
        self.sensors.remove(sensor)

    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self, data):
        for observer in self.observers:
            observer.update(data)

    def read_sensors(self):
        sensors_data = {}
        for sensor in self.sensors:
            data = sensor.read_data()
            sensors_data[type(sensor).__name__] = data
            self.notify_observers({type(sensor).__name__: data})
        return sensors_data


class SensorObserver(ABC):
    """
    Абстрактный класс для наблюдателя сенсоров.
    """

    @abstractmethod
    def update(self, data):
        pass


# Пример использования
if __name__ == "__main__":
    class DroneControlSystem(SensorObserver):
        def update(self, data):
            print(f"Received sensor data: {data}")

    # Инициализация менеджера сенсоров
    sensor_manager = SensorManager()

    # Добавление наблюдателя
    sensor_manager.add_observer(DroneControlSystem())

    # Добавление сенсоров
    altimeter = Altimeter()
    gps_sensor = GPSSensor()

    sensor_manager.add_sensor(altimeter)
    sensor_manager.add_sensor(gps_sensor)

    # Чтение данных сенсоров
    sensor_data = sensor_manager.read_sensors()
    print(sensor_data)