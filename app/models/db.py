import os
import pymysql
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env de la raíz
load_dotenv()

def get_db_connection():
    try:
        connection = pymysql.connect(
            host=os.getenv('DB_HOST'),
            port=int(os.getenv('DB_PORT', 3306)), # Lee el puerto del .env (si no existe, usa 3306)
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except pymysql.MySQLError as e:
        print(f"Error crítico al conectar a la base de datos MySQL: {e}")
        raise e