from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.pago import PagoModel

pago_bp = Blueprint('pago', __name__)

@pago_bp.route('/pago/<int:id_reserva>', methods=['GET', 'POST'])
def simular_pago(id_reserva):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    if request.method == 'POST':
        # Recibir la decisión del usuario desde los botones de simulación
        resultado = request.form.get('resultado')
        simulacion_exitosa = True if resultado == 'exito' else False
        
        exito, mensaje = PagoModel.procesar_transaccion(id_reserva, session['user_id'], simulacion_exitosa)
        
        if exito and simulacion_exitosa:
            flash(mensaje, 'success')
            return redirect(url_for('pago.comprobante', id_reserva=id_reserva))
        elif exito and not simulacion_exitosa:
            flash(mensaje, 'danger')
            return redirect(url_for('reserva.mapa_vista'))
        else:
            flash(mensaje, 'danger')
            return redirect(url_for('reserva.mapa_vista'))
    return render_template('pago.html', id_reserva=id_reserva)

@pago_bp.route('/comprobante/<int:id_reserva>')
def comprobante(id_reserva):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('comprobante.html', id_reserva=id_reserva, usuario=session['user_name'])