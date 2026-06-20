import os
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv('FLASK_SECRET_KEY', 'unemi_clave_secreta_temporal')

    # Importar controladores internamente (Evita importaciones circulares)
    from app.controllers.auth_controller import auth_bp
    from app.controllers.reserva_controller import reserva_bp
    from app.controllers.pago_controller import pago_bp

    # Registrar controladores
    app.register_blueprint(auth_bp)
    app.register_blueprint(reserva_bp)
    app.register_blueprint(pago_bp)
    
    return app