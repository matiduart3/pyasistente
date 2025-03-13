import os
import psycopg2
from psycopg2 import sql, OperationalError
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Configuración de la base de datos
DATABASE_URL = os.getenv("DATABASE_URL")

# Conectar a la base de datos PostgreSQL
def connect_db():
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode="prefer")  # Mejor compatibilidad en Railway
        cursor = conn.cursor()
        return conn, cursor
    except OperationalError as e:
        print(f"❌ Error al conectar a la base de datos: {e}")
        return None, None  # Devolver None en caso de fallo

# Crear tabla si no existe
def create_table():
    conn, cursor = connect_db()
    if conn is None:
        return  # No intentar crear la tabla si la conexión falló
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            phone TEXT UNIQUE,
            username TEXT UNIQUE
        )
    ''')
    conn.commit()
    conn.close()
    print("✅ Tabla 'users' verificada o creada en la base de datos.")

# Obtener usuario asignado
def get_user(phone):
    conn, cursor = connect_db()
    if conn is None:
        return None  # Si la conexión falló, no hacer nada
    
    cursor.execute("SELECT username FROM users WHERE phone = %s", (phone,))
    user = cursor.fetchone()
    conn.close()
    return user[0] if user else None

# Obtener el siguiente número disponible en la secuencia
def get_next_user_number():
    conn, cursor = connect_db()
    if conn is None:
        return "001"  # Si hay error, devolver 001 por defecto
    
    cursor.execute("SELECT COALESCE(MAX(id) + 1, 1) FROM users")  # Obtener el próximo ID
    count = cursor.fetchone()[0]
    conn.close()
    return f"{count:03d}"  # Formateamos el número con tres dígitos (001, 002, 003)

# Asignar usuario único a un número
def assign_user(phone):
    existing_user = get_user(phone)
    if existing_user:
        print(f"🔍 Usuario ya existente para {phone}: {existing_user}")
        return existing_user  # Retorna el usuario si ya existe

    # Obtener el siguiente número de usuario
    user_number = get_next_user_number()
    new_username = f"usuarioganamos{user_number}"  # Ejemplo: usuarioganamos001

    print(f"🆕 Asignando nuevo usuario: {new_username} para {phone}")

    conn, cursor = connect_db()
    if conn is None:
        return None  # No hacer nada si la conexión falló

    cursor.execute("INSERT INTO users (phone, username) VALUES (%s, %s)", (phone, new_username))
    conn.commit()
    conn.close()

    return new_username

# Inicializar base de datos solo si este script es el principal
if __name__ == "__main__":
    create_table()
