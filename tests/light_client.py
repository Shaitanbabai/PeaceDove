import requests

# Модель данных
class DroneModel:
    """Класс DroneModel отвечает за хранение данных о состоянии БПЛА."""
    def __init__(self):
        self.altitude = 0  # Высота в метрах
        self.speed = 0  # Скорость в м/с
        self.position = (0, 0)  # Координаты на плоскости
        self.battery_level = 100  # Уровень заряда батареи в процентах

    def update_position(self, new_position):
        self.position = new_position

    def update_altitude(self, new_altitude):
        self.altitude = new_altitude

    def update_speed(self, new_speed):
        self.speed = new_speed

    def update_battery_level(self, consumption):
        self.battery_level -= consumption

# Представление
class DroneView:
    """Класс DroneView отвечает за визуализацию данных о состоянии БПЛА."""
    def display_status(self, model):
        print(f"Altitude: {model.altitude} meters, Speed: {model.speed} m/s, "
              f"Position: {model.position}, Battery: {model.battery_level}%")

    def alert(self, message):
        print(f"ALERT: {message}")

# Контроллер
class DroneController:
    """Класс DroneController отвечает за управление логикой работы БПЛА."""
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def change_position(self, new_position):
        self.model.update_position(new_position)
        self.view.display_status(self.model)

    def change_altitude(self, new_altitude):
        self.model.update_altitude(new_altitude)
        self.view.display_status(self.model)

    def change_speed(self, new_speed):
        self.model.update_speed(new_speed)
        self.view.display_status(self.model)

    def monitor_battery(self):
        if self.model.battery_level < 20:
            self.view.alert("Low battery! Returning to base.")
            self.return_to_base()

    def return_to_base(self):
        self.model.update_position((0, 0))
        self.model.update_altitude(0)
        self.model.update_speed(0)
        self.view.display_status(self.model)
        self.view.alert("Drone has returned to base.")

class SensorObserver:
    """Базовый класс наблюдателя за данными сенсоров."""
    def update(self, data):
        raise NotImplementedError("Метод update должен быть реализован")

class ObstacleSensor(SensorObserver):
    """Класс ObstacleSensor отвечает за обработку данных о препятствиях и управление БПЛА."""
    def __init__(self, controller):
        self.controller = controller

    def update(self, data):
        if data['distance'] < 10:
            print("Препятствие слишком близко! Изменение курса...")
            new_position = (self.controller.model.position[0] + 10, self.controller.model.position[1])
            self.controller.change_position(new_position)
        elif data['distance'] < 5:
            print("Опасное расстояние! Остановка БПЛА.")
            self.controller.change_speed(0)

class DroneState:
    """Базовый класс для различных состояний полета."""
    def handle(self, drone):
        raise NotImplementedError("Метод handle должен быть реализован")

class TakeoffState(DroneState):
    """Класс TakeoffState отвечает за состояние взлета БПЛА."""
    def handle(self, drone):
        print("Взлет...")
        drone.model.update_altitude(10)

class LandingState(DroneState):
    """Класс LandingState отвечает за состояние посадки БПЛА."""
    def handle(self, drone):
        print("Посадка...")
        drone.model.update_altitude(0)
        drone.model.update_speed(0)

class StatefulDrone:
    """Класс StatefulDrone управляет состояниями и действиями БПЛА."""
    def __init__(self, state, model, view):
        self.state = state
        self.model = model
        self.view = view

    def change_state(self, state):
        self.state = state

    def perform_action(self):
        self.state.handle(self)
        self.view.display_status(self.model)