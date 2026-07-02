# Guía de Instalación y Ejecución - MVP Completo (Sprints 1 al 4)
### Sistema de Reserva de Entradas para Concierto
**UNIVERSIDAD ESTATAL DE MILAGRO (UNEMI)** **Carrera:** Ingeniería de Software (4to Semestre - C1)  
**Grupo #8**

---

¡Hola, equipo! Esta es la guía definitiva y actualizada para levantar el proyecto completo en sus computadoras locales. Hemos completado todos los módulos (desde el Login hasta el Simulador de Pagos con Control Optimista). 

Sigan los pasos **exactamente en este orden** para evitar conflictos de bases de datos o de hilos en sus terminales.

---

## 📋 Requisitos Previos

Antes de clonar, asegúrense de tener esto instalado:
1. **Python 3.12.x** (Importante: Marcar la casilla *"Add Python to PATH"* al instalar).
2. **Git** (Usaremos estrictamente **Git Bash** para los comandos).
3. **MySQL Server** (XAMPP, MySQL Installer, o MariaDB).
4. **DBeaver** o MySQL Workbench.
5. **Visual Studio Code (VS Code)**.

---

## 🛠️ Paso 1: Clonar el Repositorio

Abran **Git Bash** en su carpeta de proyectos, clonen la rama principal y abran VS Code:

```bash
git clone <URL_DEL_REPOSITORIO_DE_GITHUB>
cd ticket_reserva_mvp
code .
```

---

## 🗄️ Paso 2: Configuración Estricta de la Base de Datos

Para que el Sprint 3 (Control Optimista) y el Sprint 4 (Pagos) funcionen, necesitamos crear la estructura relacional completa. 
**Regla de oro en DBeaver:** Ejecuten el script **bloque por bloque** (seleccionen el bloque con el mouse y presionen `Ctrl + Enter`). No ejecuten todo de golpe para evitar el error *"No database selected"*.

Abran un nuevo script SQL en DBeaver y sigan este orden:

### Bloque 1: Crear la Base de Datos
```sql
CREATE DATABASE IF NOT EXISTS unemi_concierto_db;
USE unemi_concierto_db;
```

### Bloque 2: Tablas Base (Usuarios, Eventos y Asientos)
```sql
USE unemi_concierto_db;

CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo_electronico VARCHAR(150) UNIQUE NOT NULL,
    contrasena_hash VARCHAR(255) NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS eventos (
    id_evento INT AUTO_INCREMENT PRIMARY KEY,
    nombre_evento VARCHAR(150) NOT NULL,
    fecha_hora DATETIME NOT NULL,
    lugar VARCHAR(150) NOT NULL,
    descripcion TEXT NULL,
    precio_base DECIMAL(10,2) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS asientos (
    id_asiento INT AUTO_INCREMENT PRIMARY KEY,
    numero_asiento VARCHAR(10) NOT NULL,
    seccion VARCHAR(50) NOT NULL,
    fila VARCHAR(10) NOT NULL,
    estado ENUM('DISPONIBLE', 'RESERVADO_TEMPORAL', 'VENDIDO') DEFAULT 'DISPONIBLE',
    version INT DEFAULT 0 NOT NULL,
    id_evento INT NOT NULL,
    FOREIGN KEY (id_evento) REFERENCES eventos(id_evento) ON DELETE CASCADE
) ENGINE=InnoDB;
```

### Bloque 3: Tablas Transaccionales (Reservas y Pagos)
```sql
USE unemi_concierto_db;

CREATE TABLE IF NOT EXISTS reservas (
    id_reserva INT AUTO_INCREMENT PRIMARY KEY,
    fecha_hora_reserva TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado ENUM('TEMPORAL', 'CONFIRMADA', 'CANCELADA', 'EXPIRADA') DEFAULT 'TEMPORAL',
    timestamp_expiracion DATETIME NOT NULL,
    id_usuario INT NOT NULL,
    id_asiento INT NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (id_asiento) REFERENCES asientos(id_asiento)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS pagos (
    id_pago INT AUTO_INCREMENT PRIMARY KEY,
    monto DECIMAL(10,2) NOT NULL,
    estado ENUM('PENDIENTE', 'EXITOSO', 'FALLIDO') NOT NULL,
    metodo_pago VARCHAR(50) NOT NULL,
    fecha_hora_pago DATETIME NULL,
    id_transaccion_externa VARCHAR(100) UNIQUE NULL,
    id_reserva INT NOT NULL,
    FOREIGN KEY (id_reserva) REFERENCES reservas(id_reserva)
) ENGINE=InnoDB;
```

### Bloque 4: Datos de Prueba (Mock Data)
```sql
USE unemi_concierto_db;

-- 1. Insertar el Evento
INSERT INTO eventos (id_evento, nombre_evento, fecha_hora, lugar, descripcion, precio_base)
VALUES (1, 'Gran Concierto de la UNEMI 2026', '2026-08-15 20:00:00', 'Polideportivo Milagro', 'Evento de Ingeniería de Software', 25.00)
ON DUPLICATE KEY UPDATE nombre_evento=VALUES(nombre_evento);

-- 2. Insertar Asientos de Prueba
INSERT INTO asientos (numero_asiento, seccion, fila, estado, version, id_evento) VALUES
('A-1', 'VIP', 'A', 'DISPONIBLE', 0, 1),
('A-2', 'VIP', 'A', 'DISPONIBLE', 0, 1),
('A-3', 'VIP', 'A', 'RESERVADO_TEMPORAL', 0, 1),
('A-4', 'VIP', 'A', 'VENDIDO', 0, 1),
('B-1', 'VIP', 'B', 'DISPONIBLE', 0, 1),
('B-2', 'VIP', 'B', 'DISPONIBLE', 0, 1),
('C-1', 'General', 'C', 'DISPONIBLE', 0, 1),
('C-2', 'General', 'C', 'VENDIDO', 0, 1),
('C-3', 'General', 'C', 'DISPONIBLE', 0, 1),
('D-1', 'General', 'D', 'DISPONIBLE', 0, 1),
('D-2', 'General', 'D', 'RESERVADO_TEMPORAL', 0, 1);
```

---

## 📦 Paso 3: Entorno Virtual y Librerías

Regresen a VS Code, abran la terminal de **Git Bash** en la raíz del proyecto y ejecuten esto línea por línea:

```bash
# Crear entorno virtual
python -m venv venv

# Activar el entorno (Debe aparecer (venv) en verde a la izquierda)
source venv/Scripts/activate

# Instalar dependencias exactas
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## 🔐 Paso 4: Variables de Entorno (`.env`)

Creen un archivo llamado **`.env`** en la carpeta principal del proyecto y configúrenlo con sus credenciales locales de MySQL:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=tu_usuario_aqui      # Ej: root
DB_PASSWORD=tu_clave_aqui    # Déjalo vacío si usas XAMPP sin clave
DB_NAME=unemi_concierto_db
FLASK_SECRET_KEY=unemi_software_secret_2026
```

---

## 🚀 Paso 5: Levantar el Servidor y Probar el Flujo

En su Git Bash (con el entorno activado), enciendan el servidor usando el modo interactivo para evitar que Windows lo cierre abruptamente:

```bash
python -i app.py
```

### Flujo de Pruebas:
1. **Registro:** Entren a `http://127.0.0.1:5000/register` y creen un usuario.
2. **Login:** Inicien sesión con ese usuario en `http://127.0.0.1:5000/login`.
3. **Mapa (Aforo Dinámico):** Verán los asientos verdes, amarillos y rojos cargados asíncronamente.
4. **Bloqueo Concurrente:** Den clic en un asiento Verde (Disponible). El sistema hará el `UPDATE` optimista y los enviará al simulador de pagos.
5. **Transacción ACID:** Den clic en "Simular Pago Exitoso". Verán el comprobante y el asiento pasará a ser Rojo (Vendido) definitivamente.
---
⚙️ Paso 6: Despliegue en Servidor de Producción (Waitress)
Para soportar tráfico masivo y ejecutar las pruebas de estrés, el servidor de desarrollo de Flask (Werkzeug) no es suficiente. Necesitamos levantar la aplicación con Waitress.

En su terminal de Git Bash con el entorno virtual activado, instalen la dependencia:

Bash
pip install waitress

Ejecuten el servidor de producción con 20 hilos de trabajo simultáneos.

Bash
waitress-serve --port=5000 --threads=20 --call "app:create_app"

(Nota: No verán el mensaje tradicional de colores de Flask, la consola mostrará una advertencia limpia indicando que el puerto 5000 está activo).

🦗 Paso 7: Pruebas de Estrés y Concurrencia (Locust)
Para demostrar el Control Optimista en el MVP, someteremos el sistema a un ataque de cientos de usuarios simultáneos.

Instalen Locust en el entorno virtual activo:

Bash
pip install locust

Creen un archivo llamado locustfile.py en la raíz del proyecto y peguen el script de simulación de compradores. Asegúrense de usar correos válidos y la llave contrasena en el payload de login para evitar errores 401 o 500.

Abran una nueva terminal de Git Bash, activen el entorno virtual (source venv/Scripts/activate) y ejecuten:

Bash
locust
Abran su navegador en http://localhost:8089.

Configuren la prueba en la interfaz gráfica:

Number of users: 500 (o la cantidad a simular).

Spawn rate: 20.

Host: Escriban estrictamente http://127.0.0.1:5000 (¡Sin corchetes ni barras al final!).

Hagan clic en "Start swarming" y observen en la consola cómo el motor InnoDB y Flask bloquean las condiciones de carrera (Errores HTTP 409) para evitar la sobreventa.
---

## 🛑 Buenas Prácticas de Cierre

Para no dejar hilos colgados ni puertos bloqueados al terminar de programar, sigan este proceso en su terminal de Git Bash:

1. Presionen `Ctrl + C`. (Aparecerán los símbolos `>>>`).
2. Escriban `quit()` y presionen `Enter`.
3. Desactiven el entorno virtual con:
   ```bash
   deactivate
   ```
*(Opcional: Si el CSS no carga, recuerden presionar `Ctrl + F5` en el navegador para limpiar la caché).*
