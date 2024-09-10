from abc import ABC, abstractmethod
import asyncio
import pygame
from pygame import math
import math
import queue
import threading


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
        self.__degree = None
        self.__drone = drone  # Хранит ссылку на объект DroneController
        self.__degree = degree  # Угол поворота

    async def execute(self):
        # Выполняет команду поворота на заданный угол
        await self.__drone.turn(self.__degree)

class DroneSimulator:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Drone Simulator")
        self.drone_rect = pygame.Rect(400, 500, 20, 10)
        self.clock = pygame.time.Clock()
        self.x, self.y = 400, 500  # Начальная позиция дрона
        self.command_queue = queue.Queue()

    def draw(self):
        self.screen.fill((255, 255, 255))
        pygame.draw.rect(self.screen, (0, 0, 255), self.drone_rect)
        pygame.display.flip()
        self.drone_rect.center = (self.x, self.y)

    async def update(self, command: ICommand):
        await command.execute()
        if isinstance(command, MoveForward):
            self.y -= command.__distance  # Движение вверх по оси Y (можно изменить)
        elif isinstance(command, Turn):
            # Поворот на угол degree
            angle = math.radians(command.__degree)
            self.x += math.cos(angle) * 10
            self.y -= math.sin(angle) * 10  # Движение вверх по оси Y (можно изменить)
        self.draw()

# Пример использования
async def main():
    drone = DroneController()
    simulator = DroneSimulator()
    takeoff_command = Takeoff(drone)
    move_command = MoveForward(drone, 10)
    turn_command = Turn(drone, 90)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        await takeoff_command.execute()
        await move_command.execute()
        await turn_command.execute()

        simulator.clock.tick(60)


if __name__ == "__main__":
    asyncio.run(main())
# asyncio.run(main())  # Закомментировано для предотвращения автоматического запуска
