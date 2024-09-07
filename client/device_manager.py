from abc import ABC, abstractmethod
import logging
import cv2
import subprocess
from flask import Flask, Response, render_template


app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class DeviceManager:
    """Менеджер для управления устройствами, такими как камеры."""

    def __init__(self):
        """Инициализация менеджера устройств."""
        self.logger = logging.getLogger(self.__class__.__name__)
        self.devices = []
        self.camera_device = None

    def register_device(self, device):
        """Регистрация нового устройства."""
        self.devices.append(device)
        self.logger.info(f"Device {device.get_name()} registered.")

    def initialize_devices(self):
        """Инициализация всех зарегистрированных устройств."""
        self.logger.info("Инициализация всех зарегистрированных устройств.")
        for device in self.devices:
            device.initialize()

    def process_device_data(self):
        """Обработка данных от всех зарегистрированных устройств."""
        self.logger.info("Обработка данных от всех зарегистрированных устройств.")
        for device in self.devices:
            device.process_data()

    def start_video_capture(self, source="udp://127.0.0.1:1234"):
        """Инициализирует захват видео с указанного источника."""
        self.logger.info("Начинаю захват видео.")
        self.camera_device = Camera(source)
        self.camera_device.initialize()

    def stop_video_capture(self):
        """Останавливает захват видео и освобождает ресурсы."""
        self.logger.info("Останавливаю захват видео и освобождаю ресурсы.")
        if self.camera_device:
            self.camera_device.stop_streaming()
            self.camera_device = None

    def video_stream(self):
        """Генерирует поток видео кадров."""
        self.logger.info("Начинаю трансляцию видео.")
        if self.camera_device is not None and self.camera_device.capture.isOpened():
            while True:
                ret, frame = self.camera_device.capture.read()
                if not ret:
                    self.logger.warning("Не удалось получить кадр.")
                    break
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

class Device(ABC):
    """Абстрактный класс для устройств."""

    @abstractmethod
    def get_name(self):
        """Возвращает имя устройства."""
        pass

    @abstractmethod
    def initialize(self):
        """Инициализация устройства."""
        pass

    @abstractmethod
    def process_data(self):
        """Обработка данных устройства."""
        pass

class Camera(Device):
    """Класс, представляющий камеру."""

    def __init__(self, address="udp://127.0.0.1:1234"):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.capture = None
        self.ffmpeg = None
        self.address = address

    def get_name(self):
        """Возвращает имя устройства камеры."""
        return "Camera"

    def initialize(self):
        """Инициализация камеры и настройка потокового видео."""
        self.logger.info("Инициализирую камеру.")
        self.capture = cv2.VideoCapture(0)
        if not self.capture.isOpened():
            self.logger.error("Камера не может быть открыта.")
            raise Exception("Камера не может быть открыта.")

        resolution = f"{int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))}x{int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))}"
        frame_rate = f"{int(self.capture.get(cv2.CAP_PROP_FPS))}"
        codec = 'libx264'
        preset = 'ultrafast'
        output_format = "mpegts"

        settings = [
            "ffmpeg",
            "-loglevel", "debug",
            "-fflags", "nobuffer",
            "-y",
            "-f", "rawvideo",
            "-pix_fmt", "bgr24",
            "-s", resolution,
            "-r", frame_rate,
            "-i", "-", "-an",
            "-c:v", codec,
            "-preset", preset,
            "-f", output_format,
            self.address
        ]
        self.logger.debug(f"FFmpeg settings: {settings}")
        self.ffmpeg = subprocess.Popen(settings, stdin=subprocess.PIPE)
        self.logger.info("Камера инициализирована.")

    def process_data(self):
        """Обработка данных с камеры и передача их в поток."""
        if self.capture is None or self.ffmpeg is None:
            self.logger.error("Камера не инициализирована.")
            raise Exception("Камера не инициализирована.")

        self.logger.info("Обрабатываю данные с камеры.")
        ret, frame = self.capture.read()
        if not ret:
            self.logger.warning("Не удалось получить кадр.")
            return

        self.ffmpeg.stdin.write(frame.tobytes())

    def stop_streaming(self):
        """Остановка потокового видео."""
        self.logger.info("Прекращаю потоковое видео.")
        if self.capture:
            self.capture.release()
        if self.ffmpeg:
            self.ffmpeg.stdin.flush()
            self.ffmpeg.stdin.close()
            self.ffmpeg.wait()
        self.logger.info("Потоковое видео прекращено.")

class OtherDevice(Device):
    """Заглушка для других потенциальных устройств."""

    def get_name(self):
        """Возвращает имя заглушки устройства."""
        return "OtherDevice"

    def initialize(self):
        """Инициализация заглушки устройства."""
        logging.info("Инициализирую другое устройство.")
        # Код для инициализации устройства
        logging.info("Другое устройство инициализировано.")

    def process_data(self):
        """Обработка данных с заглушки устройства."""
        # Код для обработки данных устройства
        logging.info("Обрабатываю данные с другого устройства.")

device_manager = DeviceManager()

@app.route('/video_feed')
def video_feed():
    return Response(device_manager.video_stream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start')
def start():
    logging.info("Starting video capture via HTTP request.")
    device_manager.start_video_capture()
    return "Начат захват видео."

@app.route('/stop')
def stop():
    logging.info("Прекращаю захват видео.")
    device_manager.stop_video_capture()
    return "Захват видео завершен."

if __name__ == '__main__':
    app.run(debug=True)
