import sqlite3
from config import DATABASE_FILE

# Conectar a la base de datos SQLite
def connect_db():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    return conn, cursor

# Crear tabla si no existe
def create_table():
    conn, cursor = connect_db()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    cursor.execute("SELECT username FROM users WHERE phone = ?", (phone,))
    user = cursor.fetchone()
    conn.close()
    return user[0] if user else None

# Obtener el siguiente número disponible en la secuencia
def get_next_user_number():
    conn, cursor = connect_db()
    cursor.execute("SELECT COUNT(*) FROM users")  # Contamos cuántos usuarios hay
    count = cursor.fetchone()[0] + 1  # El siguiente número es el total actual + 1
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
    cursor.execute("INSERT INTO users (phone, username) VALUES (?, ?)", (phone, new_username))
    conn.commit()
    conn.close()

    return new_username

# Inicializar base de datos al ejecutar
create_table()
