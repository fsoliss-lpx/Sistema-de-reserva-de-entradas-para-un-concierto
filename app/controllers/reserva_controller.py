from flask import Blueprint, render_template, jsonify, session, redirect, url_for
from app.models.db import get_db_connection
from app.models.asiento import AsientoModel
from flask import request 

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

@reserva_bp.route('/api/reservar', methods=['POST'])
def reservar_asiento():
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'No autenticado'}), 401
        
    data = request.get_json()
    id_asiento = data.get('id_asiento')
    
    # Obtener estado y versión actual
    asiento = AsientoModel.obtener_por_id(id_asiento)
    if not asiento:
        return jsonify({'status': 'error', 'message': 'Asiento no encontrado'}), 404
        
    if asiento['estado'] != 'DISPONIBLE':
        return jsonify({'status': 'error', 'message': 'El asiento ya no está disponible'}), 409

    # Intentar ejecutar el bloqueo optimista en MySQL
    exito = AsientoModel.intentar_reservar(id_asiento, session['user_id'], asiento['version'])
    
    if exito:
        return jsonify({'status': 'success', 'message': '¡Asiento bloqueado temporalmente por 10 minutos!'}), 200
    else:
        return jsonify({
            'status': 'error', 
            'message': '¡Condición de Carrera! Otro usuario acaba de tomar este asiento.'
        }), 409

