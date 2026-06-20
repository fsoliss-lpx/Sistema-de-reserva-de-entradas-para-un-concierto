from app.models.db import get_db_connection
from datetime import datetime

class PagoModel:
    @staticmethod
    def procesar_transaccion(id_reserva, id_usuario, simulacion_exitosa):
        """
        Ejecuta una transacción ACID completa.
        - Éxito: Reserva -> CONFIRMADA, Asiento -> VENDIDO.
        - Fallo: Reserva -> CANCELADA, Asiento -> DISPONIBLE.
        """
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                # 1. Validar propiedad y estado de la reserva
                cursor.execute("SELECT id_asiento, estado FROM reservas WHERE id_reserva = %s AND id_usuario = %s", (id_reserva, id_usuario))
                reserva = cursor.fetchone()
                if not reserva or reserva['estado'] != 'TEMPORAL':
                    return False, "La reserva no es válida o su tiempo ya expiró."
                
                id_asiento = reserva['id_asiento']
                fecha_pago = datetime.now()
                if simulacion_exitosa:
                    # Escenario A: Compra Exitosa (RF-05)
                    cursor.execute("UPDATE reservas SET estado = 'CONFIRMADA' WHERE id_reserva = %s", (id_reserva,))
                    cursor.execute("UPDATE asientos SET estado = 'VENDIDO' WHERE id_asiento = %s", (id_asiento,))
                    cursor.execute("INSERT INTO pagos (monto, estado, metodo_pago, fecha_hora_pago, id_reserva) VALUES (25.00, 'EXITOSO', 'Simulador Local', %s, %s)", (fecha_pago, id_reserva))
                    mensaje = "Transacción aprobada. Comprobante generado."
                else:
                    # Escenario B: Expiración o Fallo Financiero
                    cursor.execute("UPDATE reservas SET estado = 'CANCELADA' WHERE id_reserva = %s", (id_reserva,))
                    cursor.execute("UPDATE asientos SET estado = 'DISPONIBLE' WHERE id_asiento = %s", (id_asiento,))
                    cursor.execute("INSERT INTO pagos (monto, estado, metodo_pago, fecha_hora_pago, id_reserva) VALUES (25.00, 'FALLIDO', 'Simulador Local', %s, %s)", (fecha_pago, id_reserva))
                    mensaje = "Transacción rechazada. El asiento ha sido liberado."
                    
            # Confirmar operaciones atómicas
            connection.commit()
            return True, mensaje
        except Exception as e:
            # Reversión automática en caso de error (Rollback)
            connection.rollback()
            print(f"Error transaccional en pago: {e}")
            return False, "Error interno del servidor durante el pago."
        finally:
            connection.close()