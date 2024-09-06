from flask import Flask
from flask_jwt_extended import JWTManager
from drone_routes import drone_routes

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'
jwt = JWTManager(app)

app.register_blueprint(drone_routes)

if __name__ == '__main__':
    app.run(debug=True)