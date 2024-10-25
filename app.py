from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def registro():
    return render_template('registro.html')

@app.route('/procesar_registro', methods=['POST'])
def procesar_registro():
    # Recoge los datos del formulario
    nombres_apellidos = request.form['nombres_apellidos']
    alias = request.form['alias']
    genero = request.form['genero']
    zona_residencia = request.form['zona_residencia']
    estado = request.form['estado']
    urbanizacion = request.form['urbanizacion']
    tipo_documento = request.form['tipo_documento']
    numero_documento = request.form['numero_documento']
    numero_principal = request.form['numero_principal']
    numero_secundario = request.form['numero_secundario']
    correo = request.form['correo']
    nombre_emprendimiento = request.form['nombre_emprendimiento']
    instagram_emprendimiento = request.form['instagram_emprendimiento']
    referido_nombre = request.form['referido_nombre']
    referido_telefono = request.form['referido_telefono']

    # Conectar con la base de datos y guardar los datos
    conn = sqlite3.connect('solicitudes.db')
    c = conn.cursor()
    c.execute(''' 
        INSERT INTO usuarios (nombres_apellidos, alias, genero, zona_residencia, estado, urbanizacion, tipo_documento, 
        numero_documento, numero_principal, numero_secundario, correo, nombre_emprendimiento, instagram_emprendimiento, 
        referido_nombre, referido_telefono) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (nombres_apellidos, alias, genero, zona_residencia, estado, urbanizacion, tipo_documento, numero_documento, 
          numero_principal, numero_secundario, correo, nombre_emprendimiento, instagram_emprendimiento, referido_nombre, 
          referido_telefono))
    conn.commit()
    conn.close()

    return redirect(url_for('registro_exitoso', nombre_usuario=nombres_apellidos))

@app.route('/registro_exitoso')
def registro_exitoso():
    # Aquí se necesita recibir el nombre del usuario
    nombre_usuario = request.args.get('nombre_usuario')  # Obtener el nombre del usuario
    return render_template('registro_exitoso.html', nombre_usuario=nombre_usuario)


@app.route('/admin')
def admin():
    # Conectar con la base de datos y obtener los datos de los usuarios
    conn = sqlite3.connect('solicitudes.db')
    c = conn.cursor()
    c.execute('SELECT * FROM usuarios')
    solicitudes = c.fetchall()
    conn.close()
    
    return render_template('admin.html', solicitudes=solicitudes)

# Aquí va el bloque que arranca la aplicación
if __name__ == '__main__':
    app.run(debug=True, port=5001)

