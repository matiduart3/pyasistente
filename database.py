import os
import psycopg2
from psycopg2 import OperationalError
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Configuración de la base de datos
DATABASE_URL = os.getenv("DATABASE_URL")

# Validar que la variable DATABASE_URL esté cargada
if not DATABASE_URL:
    print("❌ ERROR: La variable DATABASE_URL no está definida en Railway.")
else:
    print(f"✅ Conectando a la base de datos: {DATABASE_URL}")

# Conectar a la base de datos PostgreSQL
def connect_db():
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode="require")  # Modo seguro
        cursor = conn.cursor()
        return conn, cursor
    except OperationalError as e:
        print(f"❌ ERROR al conectar a la base de datos: {e}")
        return None, None  # Devuelve None si hay un error

# Crear tabla si no existe
def create_table():
    conn, cursor = connect_db()
    if conn is None:
        print("⚠️ No se pudo crear la tabla porque la conexión falló.")
        return  
    
    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                phone TEXT UNIQUE NOT NULL,
                username TEXT UNIQUE NOT NULL
            )
        ''')
        conn.commit()
        print("✅ Tabla 'users' verificada o creada en PostgreSQL.")
    except Exception as e:
        print(f"❌ ERROR al crear la tabla: {e}")
    finally:
        conn.close()

# Obtener usuario asignado
def get_user(phone):
    conn, cursor = connect_db()
    if conn is None:
        return None  
    
    try:
        cursor.execute("SELECT username FROM users WHERE phone = %s", (phone,))
        user = cursor.fetchone()
        return user[0] if user else None
    except Exception as e:
        print(f"⚠️ ERROR al obtener usuario: {e}")
        return None
    finally:
        conn.close()

# Obtener el siguiente número disponible
def get_next_user_number():
    conn, cursor = connect_db()
    if conn is None:
        return "001"  
    
    try:
        cursor.execute("SELECT COUNT(*) FROM users")  
        count = cursor.fetchone()[0] + 1  
        return f"{count:03d}"  
    except Exception as e:
        print(f"⚠️ ERROR al obtener el siguiente usuario: {e}")
        return "001"  
    finally:
        conn.close()

# Asignar usuario único
def assign_user(phone):
    if not phone:
        print("⚠️ ERROR: No se recibió un número de teléfono válido.")
        return None  

    existing_user = get_user(phone)
    if existing_user:
        print(f"🔍 Usuario ya existente para {phone}: {existing_user}")
        return existing_user  

    user_number = get_next_user_number()
    new_username = f"usuarioganamos{user_number}"  

    print(f"🆕 Asignando nuevo usuario: {new_username} para {phone}")

    conn, cursor = connect_db()
    if conn is None:
        return None  

    try:
        cursor.execute("INSERT INTO users (phone, username) VALUES (%s, %s)", (phone, new_username))
        conn.commit()
        return new_username
    except Exception as e:
        print(f"❌ ERROR al asignar usuario: {e}")
        return None
    finally:
        conn.close()

# Inicializar base de datos si el script es el principal
if __name__ == "__main__":
    create_table()
