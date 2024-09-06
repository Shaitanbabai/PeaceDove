from abc import ABC, abstractmethod
import asyncio

# Класс для управления дроном, включает методы для выполнения основных команд
class DroneController:
    """
    Класс для управления дроном. Содержит методы для взлета, движения вперед и поворотов.
    """

    async def takeoff(self):
        """
        Асинхронная команда для взлета дрона.
        """
        print('Дрон взлетает...')
        await asyncio.sleep(1)  # Имитируем задержку

    async def move_forward(self, distance: float):
        """
        Асинхронная команда для движения вперед на заданное расстояние.
        :param distance: Расстояние, на которое дрон должен пролететь вперед.
        """
        print(f"Летим вперед на {distance} метров")
        await asyncio.sleep(1)  # Имитируем задержку

    async def turn(self, degree: float):
        """
        Асинхронная команда для поворота дрона на заданное количество градусов.
        :param degree: Угол поворота в градусах.
        """
        print(f"Поворачиваем на {degree} градусов")
        await asyncio.sleep(1)  # Имитируем задержку

# Интерфейс команды, определяет метод execute
class ICommand(ABC):
    @abstractmethod
    async def execute(self):
        """
        Асинхронный метод для выполнения команды.
        """
        pass

# Команда для взлета дрона
class Takeoff(ICommand):
    def __init__(self, drone: DroneController):
        self.__drone = drone  # Хранит ссылку на объект DroneController

    async def execute(self):
        # Выполняет команду взлета
        await self.__drone.takeoff()

# Команда для движения дрона вперед
class MoveForward(ICommand):
    def __init__(self, drone: DroneController, distance: float):
        self.__drone = drone  # Хранит ссылку на объект DroneController
        self.__distance = distance  # Расстояние для движения вперед

    async def execute(self):
        # Выполняет команду движения вперед на заданное расстояние
        await self.__drone.move_forward(self.__distance)

# Команда для поворота дрона
class Turn(ICommand):
    def __init__(self, drone: DroneController, degree: float):
        self.__drone = drone  # Хранит ссылку на объект DroneController
        self.__degree = degree  # Угол поворота

    async def execute(self):
        # Выполняет команду поворота на заданный угол
        await self.__drone.turn(self.__degree)

# Пример использования
async def main():
    drone = DroneController()
    takeoff_command = Takeoff(drone)
    move_command = MoveForward(drone, 10)
    turn_command = Turn(drone, 90)

    await takeoff_command.execute()
    await move_command.execute()
    await turn_command.execute()

# asyncio.run(main())  # Закомментировано для предотвращения автоматического запуска
