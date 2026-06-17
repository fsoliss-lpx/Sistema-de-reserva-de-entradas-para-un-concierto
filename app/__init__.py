import os
from flask import Flask

def create_app():
    app = Flask(__name__)

    # Configurar la clave secreta
    app.secret_key = os.getenv('FLASK_SECRET_KEY', 'unemi_clave_secreta_temporal')

    # Importar los controladores (Blueprints)
    from app.controllers.auth_controller import auth_bp

    # Registrar los Blueprints
    app.register_blueprint(auth_bp)
    
    return app