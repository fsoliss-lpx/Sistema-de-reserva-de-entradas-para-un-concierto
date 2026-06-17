from app.models.db import get_db_connection
from werkzeug.security import generate_password_hash

class UsuarioModel:
    @staticmethod
    def crear_usuario(nombre, correo, contrasena):
        """
        Registra un usuario aplicando hashing criptográfico a la contraseña (RNF-02).
        Garantiza que el correo electrónico sea un atributo único en la persistencia.
        """
        # Generar hash seguro de la contraseña
        contrasena_segura = generate_password_hash(contrasena)
        
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                    INSERT INTO usuarios (nombre, correo_electronico, contrasena_hash) 
                    VALUES (%s, %s, %s)
                """
                cursor.execute(sql, (nombre, correo, contrasena_segura))
            # Guardar transaccionalmente bajo soporte ACID de InnoDB
            connection.commit()
            return True
        except Exception as e:
            # Si el correo ya existe, saltará un error por el atributo UNIQUE
            print(f"Error al registrar el usuario en el modelo: {e}")
            return False
        finally:
            connection.close()

    @staticmethod
    def buscar_por_correo(correo):
        """
        Busca y retorna los datos de un usuario por su correo electrónico.
        """
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM usuarios WHERE correo_electronico = %s"
                cursor.execute(sql, (correo,))
                return cursor.fetchone()
        finally:
            connection.close()