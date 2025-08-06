# database.py
import sqlite3  # Importamos la librería para manejar bases de datos SQLite

# Nombre del archivo donde se guarda la base de datos
DATABASE = 'pacientes.db'

# --- Función para conectarse a la base de datos ---
def get_db():
    # Conectamos a la base de datos (o la crea si no existe)
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Esto permite acceder a los datos como si fueran diccionarios
    return conn

# --- Función que crea las tablas si no existen ---
def init_db():
    db = get_db()
    cursor = db.cursor()

    # Creamos la tabla de áreas (como las especialidades médicas)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS areas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE
        );
    """)

    # Creamos la tabla de pacientes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            edad INTEGER,
            estado TEXT NOT NULL DEFAULT 'Pendiente',
            area_id INTEGER,
            FOREIGN KEY (area_id) REFERENCES areas (id)
        );
    """)

    # Checamos si ya hay áreas, y si no, las insertamos
    cursor.execute("SELECT COUNT(id) FROM areas")
    if cursor.fetchone()[0] == 0:
        especialidades = [
            'Cardiología', 'Dermatología', 'Ginecología', 
            'Medicina General', 'Neurología', 'Oftalmología', 
            'Pediatría', 'Traumatología', 'Urgencias', 'Dentista'
        ]
        # Insertamos todas las áreas de una
        cursor.executemany("INSERT INTO areas (nombre) VALUES (?)", [(esp,) for esp in especialidades])

    db.commit()  # Guardamos los cambios
    db.close()   # Cerramos la conexión

# --- Función para obtener todas las áreas (ordenadas por nombre) ---
def get_areas():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id, nombre FROM areas ORDER BY nombre")
    areas = cursor.fetchall()  # Trae todos los resultados
    db.close()
    return areas

# --- Función para agregar un nuevo paciente ---
def add_paciente(nombre, edad, area_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO pacientes (nombre, edad, area_id, estado) VALUES (?, ?, ?, 'Pendiente')",
        (nombre, edad, area_id)
    )
    db.commit()
    db.close()

# --- Función para obtener los pacientes según filtros (estado, área y nombre) ---
def get_pacientes(estado_filtro=None, area_filtro=None, nombre_busqueda=None):
    """Devuelve la lista de pacientes, con filtros si se usan."""
    db = get_db()
    cursor = db.cursor()
    
    # Query base (esto es como el esqueleto de la búsqueda)
    query = """
        SELECT p.id, p.nombre, p.edad, p.estado, a.nombre as area 
        FROM pacientes p 
        JOIN areas a ON p.area_id = a.id 
        WHERE 1=1
    """
    params = []  # Acá guardamos los datos que vamos a pasar a la consulta

    # Si se quiere filtrar por estado (Pendiente o Atendido)
    if estado_filtro and estado_filtro != 'Todas':
        query += " AND p.estado = ?"
        params.append(estado_filtro)
    
    # Si se quiere filtrar por área (Cardiología, etc.)
    if area_filtro and area_filtro != 'Todas':
        query += " AND a.nombre = ?"
        params.append(area_filtro)

    # Si se busca por nombre (ej: "Juan")
    if nombre_busqueda:
        query += " AND p.nombre LIKE ?"
        params.append(f"%{nombre_busqueda}%")  # Agrega los % para que funcione como búsqueda parcial
    
    # Ordenamos por ID descendente (los más nuevos primero)
    query += " ORDER BY p.id DESC"
    
    cursor.execute(query, params)
    pacientes = cursor.fetchall()
    db.close()
    return pacientes

# --- Función para marcar un paciente como "Atendido" ---
def marcar_como_atendido(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("UPDATE pacientes SET estado = 'Atendido' WHERE id = ?", (id,))
    db.commit()
    db.close()

# --- Función para eliminar un paciente de la base de datos ---
def delete_paciente(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM pacientes WHERE id = ?", (id,))
    db.commit()
    db.close()
