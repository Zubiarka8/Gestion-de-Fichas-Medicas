# database.py
import sqlite3

DATABASE = 'pacientes.db'

# --- get_db y init_db (sin cambios) ---
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS areas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE
        );
    """)
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
    cursor.execute("SELECT COUNT(id) FROM areas")
    if cursor.fetchone()[0] == 0:
        especialidades = [
            'Cardiología', 'Dermatología', 'Ginecología', 
            'Medicina General', 'Neurología', 'Oftalmología', 
            'Pediatría', 'Traumatología', 'Urgencias', 'Dentista'
        ]
        cursor.executemany("INSERT INTO areas (nombre) VALUES (?)", [(esp,) for esp in especialidades])
    db.commit()
    db.close()

# --- get_areas y add_paciente (sin cambios) ---
def get_areas():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id, nombre FROM areas ORDER BY nombre")
    areas = cursor.fetchall()
    db.close()
    return areas

def add_paciente(nombre, edad, area_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO pacientes (nombre, edad, area_id, estado) VALUES (?, ?, ?, 'Pendiente')",
        (nombre, edad, area_id)
    )
    db.commit()
    db.close()


# === FUNCIÓN MODIFICADA ===
def get_pacientes(estado_filtro=None, area_filtro=None, nombre_busqueda=None):
    """Obtiene los pacientes aplicando filtros de estado, área y AHORA búsqueda por nombre."""
    db = get_db()
    cursor = db.cursor()
    
    query = """
        SELECT p.id, p.nombre, p.edad, p.estado, a.nombre as area 
        FROM pacientes p 
        JOIN areas a ON p.area_id = a.id 
        WHERE 1=1
    """
    params = []

    if estado_filtro and estado_filtro != 'Todas':
        query += " AND p.estado = ?"
        params.append(estado_filtro)
    
    if area_filtro and area_filtro != 'Todas':
        query += " AND a.nombre = ?"
        params.append(area_filtro)

    # --- NUEVO BLOQUE PARA BÚSQUEDA POR NOMBRE ---
    if nombre_busqueda:
        query += " AND p.nombre LIKE ?"
        params.append(f"%{nombre_busqueda}%") # Usamos % para búsqueda parcial
    
    query += " ORDER BY p.id DESC"
    
    cursor.execute(query, params)
    pacientes = cursor.fetchall()
    db.close()
    return pacientes


# --- marcar_como_atendido y delete_paciente (sin cambios) ---
def marcar_como_atendido(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("UPDATE pacientes SET estado = 'Atendido' WHERE id = ?", (id,))
    db.commit()
    db.close()

def delete_paciente(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM pacientes WHERE id = ?", (id,))
    db.commit()
    db.close()