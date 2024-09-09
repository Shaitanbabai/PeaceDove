import pytest
import logging
import subprocess
import psutil

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class DroneModel:
    """Модель дрона, содержащая его состояние."""

    def __init__(self):
        """Инициализация модели дрона."""
        self.altitude = 0
        self.speed = 0
        self.position = (0, 0)
        self.battery_level = 100


class DroneView:
    """Представление дрона для отображения его состояния."""

    def display_status(self, model):
        """Отображает текущий статус дрона.

        Args:
            model (DroneModel): Модель дрона для отображения.
        """
        logging.info(
            f"Altitude: {model.altitude}, Speed: {model.speed}, Position: {model.position}, Battery: {model.battery_level}%")


class DroneController:
    """Контроллер дрона для управления его состоянием."""

    def __init__(self, model, view):
        """Инициализация контроллера дрона.

        Args:
            model (DroneModel): Модель дрона.
            view (DroneView): Представление дрона.
        """
        self.model = model
        self.view = view

    def change_position(self, new_position):
        """Изменяет позицию дрона.

        Args:
            new_position (tuple): Новая позиция дрона.
        """
        self.model.position = new_position
        self.view.display_status(self.model)

    def change_altitude(self, new_altitude):
        """Изменяет высоту дрона.

        Args:
            new_altitude (int): Новая высота дрона.
        """
        self.model.altitude = new_altitude
        self.view.display_status(self.model)

    def change_speed(self, new_speed):
        """Изменяет скорость дрона.

        Args:
            new_speed (int): Новая скорость дрона.
        """
        self.model.speed = new_speed
        self.view.display_status(self.model)

    def monitor_battery(self):
        """Мониторинг уровня заряда батареи дрона."""
        if self.model.battery_level < 20:
            self.land()

    def land(self):
        """Посадка дрона."""
        self.model.position = (0, 0)
        self.view.display_status(self.model)


class DroneFactory:
    """Фабрика для создания дронов."""

    @staticmethod
    def create_drone():
        """Создает и возвращает новый дрон.

        Returns:
            DroneController: Контроллер дрона.
        """
        model = DroneModel()
        view = DroneView()
        controller = DroneController(model, view)
        return controller


@pytest.fixture
def setup_drone():
    """Фикстура для настройки дрона.

    Returns:
        DroneController: Контроллер дрона.
    """
    return DroneFactory.create_drone()


def test_initial_state(setup_drone):
    """Тест начального состояния дрона."""
    controller = setup_drone
    logging.info("Testing initial state")
    assert controller.model.altitude == 0
    assert controller.model.speed == 0
    assert controller.model.position == (0, 0)
    assert controller.model.battery_level == 100


def test_change_position(setup_drone):
    """Тест изменения позиции дрона."""
    controller = setup_drone
    logging.info("Testing change position")
    controller.change_position((10, 20))
    assert controller.model.position == (10, 20)


def test_change_altitude(setup_drone):
    """Тест изменения высоты дрона."""
    controller = setup_drone
    logging.info("Testing change altitude")
    controller.change_altitude(100)
    assert controller.model.altitude == 100


def test_change_speed(setup_drone):
    """Тест изменения скорости дрона."""
    controller = setup_drone
    logging.info("Testing change speed")
    controller.change_speed(50)
    assert controller.model.speed == 50


def test_battery_monitor(setup_drone):
    """Тест мониторинга батареи дрона."""
    controller = setup_drone
    logging.info("Testing battery monitor")
    controller.model.battery_level = 15
    controller.monitor_battery()
    assert controller.model.position == (0, 0)


def run_tests():
    """Функция для запуска тестов и мониторинга ресурсов."""
    try:
        # Начало мониторинга системных ресурсов
        process = psutil.Process()
        cpu_usage_before = process.cpu_percent(interval=None)
        memory_usage_before = process.memory_info().rss

        # Запуск тестов с помощью pytest
        subprocess.run(['pytest', __file__], check=True)

        # Завершение мониторинга системных ресурсов
        cpu_usage_after = process.cpu_percent(interval=None)
        memory_usage_after = process.memory_info().rss

        logging.info(f"CPU usage during tests: {cpu_usage_after - cpu_usage_before}%")
        logging.info(f"Memory usage during tests: {memory_usage_after - memory_usage_before} bytes")
    except subprocess.CalledProcessError as e:
        logging.error(f"Tests failed with error: {e}")
    else:
        logging.info("All tests passed successfully!")


if __name__ == "__main__":
    run_tests()
