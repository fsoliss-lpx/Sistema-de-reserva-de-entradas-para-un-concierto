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
        return jsonify({'status': 'error', 'message': 'Usuario no autenticado'}), 401
        
    data = request.get_json()
    id_asiento = data.get('id_asiento')
    
    # Buscamos el estado actual del asiento
    asiento = AsientoModel.obtener_por_id(id_asiento)
    
    if not asiento:
        return jsonify({'status': 'error', 'message': 'Asiento no encontrado'}), 404
        
    if asiento['estado'] != 'DISPONIBLE':
        return jsonify({'status': 'error', 'message': 'El asiento ya no se encuentra disponible'}), 409

    # Intentar el bloqueo concurrente (Ahora devuelve el ID de la reserva en lugar de solo True)
    id_nueva_reserva = AsientoModel.intentar_reservar(id_asiento, session['user_id'], asiento['version'])
    
    if id_nueva_reserva:
        # AGREGADO: Se incluye 'id_reserva' en la respuesta para que el JS sepa a dónde redirigir
        return jsonify({
            'status': 'success', 
            'message': 'Asiento bloqueado. Redirigiendo a pagos...', 
            'id_reserva': id_nueva_reserva
        }), 200
    else:
        return jsonify({
            'status': 'error', 
            'message': '¡Condición de Carrera detectada! Otro usuario seleccionó este asiento milisegundos antes.'
        }), 409

