import os
import psycopg2
from psycopg2 import OperationalError
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de la base de datos
DATABASE_URL = os.getenv("DATABASE_URL")

# Conectar a la base de datos PostgreSQL
def connect_db():
    try:
        print(f"✅ Conectando a la base de datos: {DATABASE_URL}")  # Para verificar en logs
        conn = psycopg2.connect(DATABASE_URL, sslmode="require")
        cursor = conn.cursor()
        return conn, cursor
    except OperationalError as e:
        print(f"❌ Error al conectar a la base de datos: {e}")
        return None, None

# Crear tabla si no existe
def create_table():
    conn, cursor = connect_db()
    if conn is None:
        return

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            phone TEXT UNIQUE,
            username TEXT UNIQUE
        )
    ''')
    conn.commit()
    conn.close()
    print("✅ Tabla 'users' verificada o creada.")

# Asignar usuario
def assign_user(phone):
    conn, cursor = connect_db()
    if conn is None:
        return None

    cursor.execute("SELECT username FROM users WHERE phone = %s", (phone,))
    user = cursor.fetchone()

    if user:
        print(f"🔍 Usuario ya existente para {phone}: {user[0]}")
        conn.close()
        return user[0]

    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0] + 1
    new_username = f"usuarioganamos{count:03d}"

    cursor.execute("INSERT INTO users (phone, username) VALUES (%s, %s)", (phone, new_username))
    conn.commit()
    conn.close()
    print(f"🆕 Asignado {new_username} a {phone}")

    return new_username

# Inicializar base de datos al ejecutar
if __name__ == "__main__":
    create_table()
