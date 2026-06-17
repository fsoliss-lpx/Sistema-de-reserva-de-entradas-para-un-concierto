from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.usuario import UsuarioModel
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        correo = request.form.get('correo')
        contrasena = request.form.get('contrasena')

        # Intentar crear el registro mediante el modelo
        if UsuarioModel.crear_usuario(nombre, correo, contrasena):
            flash('¡Registro exitoso! Ya puedes iniciar sesión.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Error: El correo electrónico ya se encuentra registrado.', 'danger')

    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form.get('correo')
        contrasena = request.form.get('contrasena')

        # Buscar usuario en la base de datos
        user = UsuarioModel.buscar_por_correo(correo)

        # Verificar si el usuario existe y si el hash coincide de forma segura
        if user and check_password_hash(user['contrasena_hash'], contrasena):
            # Guardar datos críticos en la sesión local (RF-01)
            session['user_id'] = user['id_usuario']
            session['user_name'] = user['nombre']
            return redirect(url_for('reserva.mapa_vista')) # Redirigirá al mapa en el Sprint 2
        else:
            flash('Credenciales incorrectas. Inténtalo de nuevo.', 'danger')

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada correctamente.', 'info')
    return redirect(url_for('auth.login'))