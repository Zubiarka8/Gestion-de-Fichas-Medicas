# app.py
from flask import Flask, render_template, request, redirect, url_for
import database

app = Flask(__name__)

database.init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nombre = request.form['nombre']
        edad = request.form['edad']
        area_id = request.form['area_id']
        
        if nombre and edad and area_id:
            database.add_paciente(nombre, edad, area_id)
            
        return redirect(url_for('index'))

    # --- LÓGICA DE FILTROS Y BÚSQUEDA ---
    estado_filtro = request.args.get('estado', 'Todas')
    area_filtro = request.args.get('area', 'Todas')
    # Obtenemos el término de búsqueda de la URL
    nombre_busqueda = request.args.get('busqueda', '')
    
    # Pasamos el nuevo parámetro de búsqueda a la función
    pacientes = database.get_pacientes(estado_filtro, area_filtro, nombre_busqueda)
    areas = database.get_areas()
    
    return render_template('index.html', 
                           pacientes=pacientes, 
                           areas=areas,
                           estado_actual=estado_filtro,
                           area_actual=area_filtro,
                           # Pasamos la búsqueda actual a la plantilla para mostrarla en el input
                           busqueda_actual=nombre_busqueda)


# --- atender y eliminar (sin cambios) ---
@app.route('/atender/<int:id>')
def atender(id):
    database.marcar_como_atendido(id)
    return redirect(request.referrer or url_for('index'))

@app.route('/eliminar/<int:id>')
def eliminar(id):
    database.delete_paciente(id)
    return redirect(request.referrer or url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)