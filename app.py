from app import create_app
from app.models.db import get_db_connection

# Crear la instancia de la aplicación Flask
app = create_app()

@app.route('/')
def index():
    """
    Ruta de prueba inicial para verificar que el servidor 
    y la base de datos están conectados correctamente.
    """
    try:
        # Intentamos hacer una conexión rápida de prueba a MySQL
        db = get_db_connection()
        db.close()
        return "<h1>¡Servidor de la UNEMI Corriendo con Éxito!</h1><p>Conexión a la Base de Datos: <b>EXITOSA</b></p>"
    except Exception as e:
        return f"<h1>Servidor Corriendo</h1><p style='color:red;'>Error de conexión a la BD: {e}</p>"

if __name__ == '__main__':
    # Lanzar el servidor en modo depuración (Debug) en el puerto 5000
    app.run(debug=True, port=5000)