from abc import ABC, abstractmethod
from drone_controller import ICommand
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Интерфейс стратегии полета, определяет метод execute
class IFlightStrategy(ABC):

    @abstractmethod
    def execute(self, commands: list):
        """
        Метод для выполнения списка команд в рамках стратегии.
        :param commands: Список команд для выполнения.
        """
        pass

# Стратегия разведывательной миссии
class ReconMissionStrategy(IFlightStrategy):
    def execute(self, commands: list):
        # Выполняет разведывательную миссию, выполняя все команды в списке
        logger.info("Начало выполнения разведывательной миссии")
        for command in commands:
            command.execute()
        logger.info("Конец миссии")

# Стратегия патрульной миссии
class PatrolMissionStrategy(IFlightStrategy):
    def __init__(self, n_patrols: int):
        self.__n_patrols = n_patrols  # Количество циклов патрулирования

    def execute(self, commands: list):
        # Выполняет патрульную миссию, повторяя все команды в списке заданное количество раз
        logger.info("Начало выполнения миссии патрулирования")
        for _ in range(self.__n_patrols):
            for command in commands:
                command.execute()
            logger.info("Патрулирование выполнено")
        logger.info("Конец миссии")

# Контекст для управления стратегиями полета дрона
class DroneContext:
    """
            Инициализирует контекст управления дронами с опциональной стратегией полета.

            Args:
                strategy (IFlightStrategy, optional): Начальная стратегия полета. По умолчанию None.
            """
    def __init__(self, strategy: IFlightStrategy = None):
        self.__strategy = strategy  # Текущая стратегия полета
        self.__commands = []  # Список команд

    def set_strategy(self, strategy: IFlightStrategy):
        """
        Устанавливает стратегию полета.
        :param strategy: Объект, реализующий интерфейс IFlightStrategy.
        """
        self.__strategy = strategy

    def add_command(self, command: ICommand):
        """
        Добавляет команду в список для выполнения.
        :param command: Объект, реализующий интерфейс ICommand.
        """
        self.__commands.append(command)

    def execute(self):
        """
        Выполняет все команды, используя текущую стратегию полета.
        После выполнения команды очищает список.
        """
        self.__strategy.execute(self.__commands)
        self.__commands.clear()


# Класс менеджера миссий
class MissionManager:
    def __init__(self):
        """
        Инициализирует менеджер миссий с пустым списком валидированных дронов.
        """
        self.validated_drones = []

    def receive_validated_drones(self, valid_drones):
        """
          Принимает список валидированных дронов и инициирует симуляцию назначения миссий.

          Args:
              valid_drones (list): Список дронов, прошедших валидацию.
          """
        if not valid_drones:
            logger.error("Список валидных дронов не передан. Убедитесь, что вы передаете список из drone_manager.py.")
            return

        self.validated_drones = valid_drones
        logger.info(f"Получены валидные дроны: {self.validated_drones}")

        # Симуляция обработки полученных данных
        self.simulate_mission_assignment()

    def simulate_mission_assignment(self):
        """
                Симулирует процесс назначения миссий каждому из валидированных дронов.
                В дальнейшем с помощью ассоциируется через клиентский интерфейс со
                списком миссия и базой полетных заданий в /drone/mission_manager.py
                """
        for drone in self.validated_drones:
            drone_id = drone.get('drone_id')
            logger.info(f"Миссия успешно назначена дрону ID {drone_id}")

    def check_completeness(self, original_list, received_list):
        """
        Проверяет полноту передачи списка дронов по сравнению с оригинальным списком.

        Args:
            original_list (list): Оригинальный список дронов.
            received_list (list): Полученный список дронов.
        """
        original_ids = {drone['drone_id'] for drone in original_list}
        received_ids = {drone['drone_id'] for drone in received_list}

        if original_ids == received_ids:
            logger.info("Полнота передачи списка дронов подтверждена.")
        else:
            logger.warning("Обнаружена неполнота в передаче списка дронов.")
            logger.debug(f"Оригинальные: {original_ids}, Полученные: {received_ids}")

# Пример использования
if __name__ == "__main__":
    # Создаем объект MissionManager
    mission_manager = MissionManager()

    # Пример тестирования передачи данных и логирования
    test_drones = [{'drone_id': 1}, {'drone_id': 2}]
    mission_manager.receive_validated_drones(test_drones)

    # Проверка полноты передачи
    mission_manager.check_completeness(test_drones, mission_manager.validated_drones)