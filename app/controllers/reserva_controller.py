from flask import Blueprint, render_template, jsonify, session, redirect, url_for
from app.models.db import get_db_connection

reserva_bp = Blueprint('reserva', __name__)

@reserva_bp.route('/mapa')
def mapa_vista():
    """
    Renderiza la vista del mapa de asientos. Protegida por sesión activa.
    """
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('mapa.html')

@reserva_bp.route('/api/asientos', methods=['GET'])
def get_asientos():
    """
    API asíncrona que retorna el listado de todos los asientos del evento 1.
    """
    if 'user_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
        
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Seleccionamos los campos clave requeridos para el mapa
            sql = "SELECT id_asiento, numero_asiento, seccion, estado, version FROM asientos WHERE id_evento = 1"
            cursor.execute(sql)
            asientos = cursor.fetchall()
        return jsonify(asientos)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        connection.close()