# Importamos Flask y algunas funciones útiles para manejar la web
from flask import Flask, render_template, request, redirect, url_for

# Importamos nuestro archivo de base de datos (el que ya comentamos antes)
import database

# Creamos la app Flask (básicamente, esto arranca el servidor web)
app = Flask(__name__)

# Inicializamos la base de datos (crea tablas y mete áreas si es la primera vez)
database.init_db()

# Ruta principal: aquí se ven los pacientes y se pueden agregar nuevos
@app.route('/', methods=['GET', 'POST'])
def index():
    mensaje_error = None  # Esto va a guardar el mensaje si hay algún error

    if request.method == 'POST':
        nombre = request.form['nombre']
        edad = request.form['edad']
        area_id = request.form['area_id']

        try:
            edad = int(edad)
        except ValueError:
            edad = -1  # Edad inválida si no es un número

        # Validamos edad
        if not (0 <= edad <= 120):
            mensaje_error = "La edad debe estar entre 0 y 120 años."
        elif not nombre or not area_id:
            mensaje_error = "Todos los campos son obligatorios."
        else:
            database.add_paciente(nombre, edad, area_id)
            return redirect(url_for('index')) 

    # --- FILTROS Y BÚSQUEDA ---
    estado_filtro = request.args.get('estado', 'Todas')
    area_filtro = request.args.get('area', 'Todas')
    nombre_busqueda = request.args.get('busqueda', '')

    pacientes = database.get_pacientes(estado_filtro, area_filtro, nombre_busqueda)
    areas = database.get_areas()

    return render_template('index.html',
                           pacientes=pacientes,
                           areas=areas,
                           estado_actual=estado_filtro,
                           area_actual=area_filtro,
                           busqueda_actual=nombre_busqueda,
                           mensaje_error=mensaje_error)  # Pasamos el mensaje a la plantilla

# --- Ruta para marcar un paciente como "Atendido" ---
@app.route('/atender/<int:id>')
def atender(id):
    database.marcar_como_atendido(id)
    # Volvemos a la página anterior o al inicio si no hay referrer
    return redirect(request.referrer or url_for('index'))

# --- Ruta para eliminar un paciente ---
@app.route('/eliminar/<int:id>')
def eliminar(id):
    database.delete_paciente(id)
    return redirect(request.referrer or url_for('index'))

# Esto hace que la app se ejecute si abrimos este archivo directamente
if __name__ == '__main__':
    app.run(debug=True)  # debug=True hace que Flask te muestre errores si algo falla
