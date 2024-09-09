import logging
from abc import ABC, abstractmethod

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Abstract Base Class
class Device(ABC):
    @abstractmethod
    def execute(self):
        """Simulate the device operation."""
        pass

    @abstractmethod
    def get_telemetry(self):
        """Return telemetry data from the device."""
        pass

# Concrete Device Classes
class CameraDevice(Device):
    def __init__(self, resolution="1080p", frame_rate=30):
        self.resolution = resolution
        self.frame_rate = frame_rate

    def execute(self):
        logger.info("Camera device is streaming video.")
        return "Streaming video"

    def get_telemetry(self):
        return {"resolution": self.resolution, "frame_rate": self.frame_rate}

class AltimeterDevice(Device):
    def __init__(self, altitude=0.0):
        self.altitude = altitude

    def execute(self):
        logger.info("Altimeter device is measuring altitude.")
        return "Measuring altitude"

    def get_telemetry(self):
        return {"altitude": self.altitude}

class GPSDevice(Device):
    def __init__(self, latitude=0.0, longitude=0.0):
        self.latitude = latitude
        self.longitude = longitude

    def execute(self):
        logger.info("GPS device is determining position.")
        return "Determining position"

    def get_telemetry(self):
        return {"latitude": self.latitude, "longitude": self.longitude}

class AnemometerDevice(Device):
    def __init__(self, wind_speed=0.0):
        self.wind_speed = wind_speed

    def execute(self):
        logger.info("Anemometer device is measuring wind speed.")
        return "Measuring wind speed"

    def get_telemetry(self):
        return {"wind_speed": self.wind_speed}

# Decorator for logging execution
def log_execution(func):
    def wrapper(*args, **kwargs):
        logger.info(f"Executing {func.__name__}")
        result = func(*args, **kwargs)
        logger.info(f"Finished executing {func.__name__}")
        return result
    return wrapper

# Factory Method
class DeviceFactory:
    @staticmethod
    def create_device(device_type):
        if device_type == "camera":
            return CameraDevice()
        elif device_type == "altimeter":
            return AltimeterDevice()
        elif device_type == "gps":
            return GPSDevice()
        elif device_type == "anemometer":
            return AnemometerDevice()
        else:raise ValueError(f"Unknown device type: {device_type}")

# Testing functionality
if __name__ == "__main__":
    try:
        # Create devices using the factory
        camera = DeviceFactory.create_device("camera")
        altimeter = DeviceFactory.create_device("altimeter")
        gps = DeviceFactory.create_device("gps")
        anemometer = DeviceFactory.create_device("anemometer")

        # Execute device actions with logging
        camera_action = log_execution(camera.execute)
        altimeter_action = log_execution(altimeter.execute)
        gps_action = log_execution(gps.execute)
        anemometer_action = log_execution(anemometer.execute)

        # Test execution
        camera_action()
        altimeter_action()
        gps_action()
        anemometer_action()

        # Output telemetry data
        logger.info("Camera telemetry: %s", camera.get_telemetry())
        logger.info("Altimeter telemetry: %s", altimeter.get_telemetry())
        logger.info("GPS telemetry: %s", gps.get_telemetry())
        logger.info("Anemometer telemetry: %s", anemometer.get_telemetry())

    except Exception as e:
        logger.error(f"An error occurred: {e}")