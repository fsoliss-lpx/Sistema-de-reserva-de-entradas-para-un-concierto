import os
from flask import Flask

def create_app():
    """
    Fábrica de la aplicación (Application Factory).
    Inicializa Flask, carga configuraciones y registra las rutas.
    """
    app = Flask(__name__)
    # Configurar la clave secreta para el manejo seguro de sesiones (RF-01)
    # Si no existe en el .env, usa una por defecto por seguridad
    app.secret_key = os.getenv('FLASK_SECRET_KEY', 'unemi_clave_secreta_temporal')
    # Aquí registraremos los Blueprints (controladores) en los siguientes pasos
    # Por ahora, dejamos la app lista para retornar
    return app