from locust import HttpUser, task, between
import random

class CompradorConcierto(HttpUser):
    # Simula el tiempo que tarda una persona real en leer la pantalla antes de hacer otro clic
    wait_time = between(1, 3)

    def on_start(self):
        """
        Se ejecuta una sola vez por cada hilo de Locust para obtener la sesión.
        Usamos una lista de usuarios reales para no saturar la misma fila de MySQL.
        """
        usuarios_prueba = [
            {"correo": "pedro@unemi.edu.ec", "contrasena": "123"},
            {"correo": "allison@unemi.edu.ec", "contrasena": "123"},
            {"correo": "jorge@unemi.edu.ec", "contrasena": "123"},
            {"correo": "miguel@unemi.edu.ec", "contrasena": "123"}
        ]
        
        # Cada hilo (usuario virtual) elige una identidad al azar
        usuario_elegido = random.choice(usuarios_prueba)
        
        # Hacemos login con la llave correcta 'contrasena' para evitar el Error 500
        self.client.post("/login", data=usuario_elegido)
        
    @task(1)
    def mirar_aforo(self):
        # Simula la consulta constante del frontend para pintar los asientos
        self.client.get("/api/asientos")

    @task(3)
    def atacar_asiento(self):
        """
        Simula el intento de reserva. Al estar el peso en 3, los usuarios
        serán agresivos intentando comprar.
        """
        # Suponiendo que tienes asientos del 1 al 11 (como en el Mock Data del SQL)
        asiento_random = random.randint(1, 11)
        
        response = self.client.post("/api/reservar", json={"id_asiento": asiento_random})
        
        # Filtramos en consola para ver la magia de la concurrencia
        if response.status_code == 200:
            print(f"✅ ¡ÉXITO! Asiento {asiento_random} asegurado.")
        elif response.status_code == 409:
            print(f"🛡️ BLOQUEADO: Condición de carrera evitada en el asiento {asiento_random}.")