from flask import Flask
from config import Api_Keys
from .routes import main as main_blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_object(Api_Keys)
    
    # Import and register blueprints
    app.register_blueprint(main_blueprint)

    return app