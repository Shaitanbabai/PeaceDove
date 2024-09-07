from flask import Flask, request, jsonify

app = Flask(__name__)

# Модель данных
class DroneModel:
    def __init__(self):
        self.altitude = 0  # Высота
        self.speed = 0  # Скорость
        self.position = (0, 0)  # Координаты
        self.battery_level = 100  # Заряд батареи

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
    def display_status(self, model):
        return {
            "altitude": model.altitude,
            "speed": model.speed,
            "position": model.position,
            "battery_level": model.battery_level
        }

    def alert(self, message):
        return {"alert": message}

# Контроллер
class DroneController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def change_position(self, new_position):
        self.model.update_position(new_position)
        return self.view.display_status(self.model)

    def change_altitude(self, new_altitude):
        self.model.update_altitude(new_altitude)
        return self.view.display_status(self.model)

    def change_speed(self, new_speed):
        self.model.update_speed(new_speed)
        return self.view.display_status(self.model)

    def monitor_battery(self):
        if self.model.battery_level < 20:
            return self.view.alert("Low battery! Returning to base.")
        return {"battery_level": self.model.battery_level}

    def return_to_base(self):
        self.model.update_position((0, 0))
        self.model.update_altitude(0)
        self.model.update_speed(0)
        return self.view.alert("Drone has returned to base.")

# Создание экземпляров модели и контроллера
drone_model = DroneModel()
drone_view = DroneView()
drone_controller = DroneController(drone_model, drone_view)

# API для управления дроном
@app.route('/status', methods=['GET'])
def get_status():
    return jsonify(drone_view.display_status(drone_model))

@app.route('/position', methods=['POST'])
def update_position():
    data = request.get_json()
    new_position = data.get('position', (0, 0))
    return jsonify(drone_controller.change_position(new_position))

@app.route('/altitude', methods=['POST'])
def update_altitude():
    data = request.get_json()
    new_altitude = data.get('altitude', 0)
    return jsonify(drone_controller.change_altitude(new_altitude))

@app.route('/speed', methods=['POST'])
def update_speed():
    data = request.get_json()
    new_speed = data.get('speed', 0)
    return jsonify(drone_controller.change_speed(new_speed))

@app.route('/battery', methods=['GET'])
def check_battery():
    return jsonify(drone_controller.monitor_battery())

@app.route('/return_to_base', methods=['POST'])
def return_to_base():
    return jsonify(drone_controller.return_to_base())

if __name__ == '__main__':
    app.run(debug=True)
