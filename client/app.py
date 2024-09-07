from flask import Flask, render_template
from .device_manager import DeviceManager
from .sensor_manager import SensorManager
from .user_interface import UserInterface
from .logging_config import setup_logging
import logging

class ApplicationFacade:
    """Фасад для управления компонентами приложения.

    Этот класс инкапсулирует инициализацию и запуск всех компонентов
    приложения, таких как менеджеры устройств, датчиков и пользовательский интерфейс.
    """

    def __init__(self):
        """Инициализация фасада приложения.

        Выполняет настройку логирования и создает экземпляры всех необходимых
        менеджеров.
        """
        # Настройка логирования
        setup_logging()
        self.logger = logging.getLogger(__name__)
        self.logger.info("Setting up application components.")

        # Создание экземпляров менеджеров
        self.device_manager = DeviceManager()
        self.sensor_manager = SensorManager()
        self.user_interface = UserInterface()

    def initialize_components(self):
        """Инициализация компонентов приложения.

        Метод выполняет все необходимые действия для инициализации компонентов,
        такие как загрузка конфигураций и подключение к базам данных.
        """
        self.logger.info("Initializing components.")
        # Здесь можно добавить код для инициализации компонентов,
        # например, загрузка конфигураций, подключение к базам данных и т.д.
        self.device_manager.initialize_devices()
        self.sensor_manager.initialize_sensors()
        self.user_interface.initialize_ui()

    def run(self):
        """Запуск веб-приложения.

        Метод настраивает маршруты для Flask приложения и запускает его.
        """
        # Запуск веб-приложения
        self.logger.info("Running the web application.")
        app = Flask(__name__)

        @app.route('/')
        def index():
            """Обработчик для главной страницы.

            Возвращает HTML шаблон для главной страницы.
            """
            self.logger.info("Rendering index page.")
            return render_template('index.html')

        @app.route('/control-panel')
        def control_panel():
            """Обработчик для страницы панели управления.

            Возвращает HTML шаблон для страницы панели управления.
            """
            self.logger.info("Rendering control panel page.")
            return render_template('control_panel.html')

        # Другие маршруты и обработчики

        app.run(debug=True)

if __name__ == '__main__':
    facade = ApplicationFacade()
    facade.initialize_components()
    facade.run()
