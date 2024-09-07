from abc import ABC, abstractmethod
import logging
import cv2
from flask import Flask, Response, render_template, request, redirect, url_for


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
            try:
                device.initialize()
            except Exception as err:
                self.logger.error(f"Ошибка при инициализации устройства {device.get_name()}: {err}")

    def process_device_data(self):
        """Обработка данных от всех зарегистрированных устройств."""
        self.logger.info("Обработка данных от всех зарегистрированных устройств.")
        for device in self.devices:
            try:
                device.process_data()
            except Exception as err:
                self.logger.error(f"Ошибка при обработке данных устройства {device.get_name()}: {err}")

    def start_video_capture(self, source="udp://127.0.0.1:1234"):
        """Инициализирует захват видео с указанного источника."""
        if self.camera_device is None:
            self.logger.info("Начинаю захват видео.")
            self.camera_device = Camera(source)
            self.camera_device.initialize()
        else:
            self.logger.warning("Захват видео уже запущен.")

    def stop_video_capture(self):
        """Останавливает захват видео и освобождает ресурсы."""
        self.logger.info("Останавливаю захват видео и освобождаю ресурсы.")
        if self.camera_device:
            self.camera_device.stop_streaming()
            self.camera_device = None
        else:
            self.logger.warning("Захват видео уже остановлен.")

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
                if not ret:
                    self.logger.error("Ошибка кодирования кадра в JPEG.")
                    continue
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else:
            self.logger.error("Камера не инициализирована или не открыта для трансляции.")

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
        self.address = address

    def get_name(self):
        """Возвращает имя устройства камеры."""
        return "Camera"

    def initialize(self):
        """Инициализация камеры для захвата видео."""
        self.capture = cv2.VideoCapture(self.address)
        if not self.capture.isOpened():
            self.logger.error("Не удалось открыть поток видео.")
        else:
            self.logger.info("Камерауспешно инициализирована.")

    def process_data(self):
        """Обработка данных устройства камеры."""
        if self.capture is not None and self.capture.isOpened():
            ret, frame = self.capture.read()
            if ret:
                # Обработка кадра, если это необходимо
                self.logger.info("Кадр успешно обработан.")
            else:
                self.logger.warning("Не удалось получить кадр для обработки.")

    def stop_streaming(self):
        """Останавливает поток видео."""
        if self.capture:
            self.capture.release()
            self.logger.info("Камера остановлена.")

device_manager = DeviceManager()

@app.route('/')
def index():
    """Отображает главную страницу с видео и кнопками управления."""
    return render_template('index.html')

@app.route('/start_video', methods=['POST'])
def start_video():
    """Запускает захват видео."""
    device_manager.start_video_capture()
    return redirect(url_for('index'))

@app.route('/stop_video', methods=['POST'])
def stop_video():
    """Останавливает захват видео."""
    device_manager.stop_video_capture()
    return redirect(url_for('index'))

@app.route('/video_feed', methods=['GET'])
def video_feed():
    """Маршрут для получения потока видео."""
    return Response(device_manager.video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    try:
        app.run(debug=True)
    except Exception as e:
        logging.error(f"Ошибка при запуске приложения: {e}")