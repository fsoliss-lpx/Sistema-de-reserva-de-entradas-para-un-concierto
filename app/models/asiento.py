from app.models.db import get_db_connection
from datetime import datetime, timedelta

class AsientoModel:
    @staticmethod
    def obtener_por_id(id_asiento):
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM asientos WHERE id_asiento = %s", (id_asiento,))
                return cursor.fetchone()
        finally:
            connection.close()
    @staticmethod
    def intentar_reservar(id_asiento, id_usuario, version_actual):
        """
        Aplica el Control Optimista. Si la versión cambió en milisegundos, falla intencionalmente.
        """
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                # 1. Intentar actualizar validando la versión exacta
                sql_update = """
                    UPDATE asientos 
                    SET estado = 'RESERVADO_TEMPORAL', version = version + 1 
                    WHERE id_asiento = %s AND version = %s AND estado = 'DISPONIBLE'
                """
                filas_afectadas = cursor.execute(sql_update, (id_asiento, version_actual))
                
                # Si filas_afectadas es 0, alguien más ganó la carrera
                if filas_afectadas == 0:
                    return False

                # 2. Si ganamos el bloqueo, creamos la reserva temporal (TTL 10 minutos)
                expiracion = datetime.now() + timedelta(minutes=10)
                sql_reserva = """
                    INSERT INTO reservas (estado, timestamp_expiracion, id_usuario, id_asiento)
                    VALUES ('TEMPORAL', %s, %s, %s)
                """
                cursor.execute(sql_reserva, (expiracion, id_usuario, id_asiento))
            
            # Consolidar la transacción ACID
            connection.commit()
            return True
        except Exception as e:
            connection.rollback()
            print(f"Error en concurrencia: {e}")
            return False
        finally:
            connection.close()