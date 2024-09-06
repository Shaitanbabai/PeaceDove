from abc import ABC, abstractmethod
import airsim
import numpy as np
import cv2
from pymavlink import mavutil
import time
import asyncio


class IDroneAPI(ABC):
    def __init__(self, connect_uri=None):
        self.client = None
        self.connect_uri = connect_uri

    @abstractmethod
    async def connect(self):
        """Абстрактный метод для подключения к дрону."""
        pass

    @abstractmethod
    async def get_image(self, max_attempts=10, delay=1):
        """Абстрактный метод для получения изображения с камеры дрона."""
        pass

class AirSimAPI(IDroneAPI):
    async def connect(self):
        self.client = airsim.MultirotorClient()
        self.client.confirmConnection()
        print("Подключение через Air Sim")

    async def get_image(self, max_attempts=10, delay=1):
        responses = self.client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)])
        if responses:
            response = responses[0]
            img_1D = np.frombuffer(response.image_data_uint8, dtype=np.uint8)
            img_rgb = img_1D.reshape(response.height, response.width, 3)
            cv2.imwrite('test.jpg', img_rgb)
            print("Image saved")
        else:
            print("No images found")

class MavLinkAPI(IDroneAPI):
    async def connect(self):
        self.client = mavutil.mavlink_connection(self.connect_uri)
        self.client.wait_heartbeat()
        print("Соединение с дроном установлено")

    async def get_image(self, max_attempts=10, delay=1):
        self.client.mav.command_long_send(
            self.client.target_system,
            self.client.target_component,
            mavutil.mavlink.MAV_CMD_IMAGE_START_CAPTURE,
            0, 0, 0, 1, 0, 0, 0, 0
        )

        for _ in range(max_attempts):
            response = self.client.recv_match(type='CAMERA_IMAGE_CAPTURED', blocking=True, timeout=5)
            if response:
                print(f"Путь до фото: {response.file_path}")
                break
            else:
                print("Ожидание камеры...")
            await asyncio.sleep(delay)

class DroneAPIFactory:
    @staticmethod
    def get_drone_api(type_api, connect_uri):
        if type_api == "AirSim":
            return AirSimAPI()
        elif type_api == "MavLink":
            return MavLinkAPI(connect_uri)
