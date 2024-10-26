from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'clave_secreta_super_segura'  # Cambia esto a una clave secreta real

# Credenciales de los usuarios
usuarios = {
    'danielcn': '1234',
    'carlatg': '5678'
}

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
    # Verificar si el usuario está autenticado
    if 'username' not in session:
        flash('Por favor, inicia sesión primero.', 'warning')
        return redirect(url_for('login'))

    # Si está autenticado, carga las solicitudes
    conn = sqlite3.connect('solicitudes.db')
    c = conn.cursor()
    c.execute('SELECT * FROM usuarios')
    solicitudes = c.fetchall()
    conn.close()
    
    return render_template('admin.html', solicitudes=solicitudes)

@app.route('/dashboard')
def dashboard():
    print(session)  # Imprime el contenido de la sesión para depuración
    if 'username' not in session:
        return redirect(url_for('admin'))  # Redirige al inicio de sesión si no está autenticado
    
    # Conectar con la base de datos y obtener los datos de los usuarios
    conn = sqlite3.connect('solicitudes.db')
    c = conn.cursor()
    c.execute('SELECT * FROM usuarios')
    solicitudes = c.fetchall()
    conn.close()

    return render_template('admin.html', solicitudes=solicitudes)

def get_solicitud_por_id(id_solicitud):
    # Conectar con la base de datos y obtener la solicitud por ID
    conn = sqlite3.connect('solicitudes.db')
    c = conn.cursor()
    c.execute('SELECT * FROM usuarios WHERE id = ?', (id_solicitud,))
    solicitud = c.fetchone()
    conn.close()
    return solicitud

@app.route('/admin/detalle/<int:id_solicitud>')
def detalle_solicitud(id_solicitud):
    if 'username' not in session:
        flash('Por favor, inicia sesión primero.', 'warning')
        return redirect(url_for('login'))

    solicitud = get_solicitud_por_id(id_solicitud)
    return render_template('detalle_solicitud.html', solicitud=solicitud)


@app.route('/admin/editar/<int:id_solicitud>', methods=['GET', 'POST'])
def editar_solicitud(id_solicitud):
    solicitud = get_solicitud_por_id(id_solicitud)
    
    if request.method == 'POST':
        # Recolecta datos editados desde el formulario
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

        # Actualiza los datos en la base de datos
        conn = sqlite3.connect('solicitudes.db')
        c = conn.cursor()
        c.execute(''' 
            UPDATE usuarios SET 
                nombres_apellidos = ?, alias = ?, genero = ?, zona_residencia = ?, estado = ?, urbanizacion = ?, 
                tipo_documento = ?, numero_documento = ?, numero_principal = ?, numero_secundario = ?, 
                correo = ?, nombre_emprendimiento = ?, instagram_emprendimiento = ?, referido_nombre = ?, 
                referido_telefono = ?
            WHERE id = ?
        ''', (nombres_apellidos, alias, genero, zona_residencia, estado, urbanizacion, tipo_documento, numero_documento,
              numero_principal, numero_secundario, correo, nombre_emprendimiento, instagram_emprendimiento, 
              referido_nombre, referido_telefono, id_solicitud))
        conn.commit()
        conn.close()

        # Redirige de vuelta a la página de detalles
        return redirect(url_for('detalle_solicitud', id_solicitud=id_solicitud))

    return render_template('editar_solicitud.html', solicitud=solicitud)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Validación simple de usuario y contraseña
        if (username == 'danielcn' and password == '1234') or (username == 'carlatg' and password == '5678'):
            session['username'] = username  # Crear sesión
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('admin'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)  # Eliminar la sesión
    flash('Has cerrado sesión.', 'info')
    return redirect(url_for('login'))

@app.route('/buscar_por_cedula', methods=['GET'])
def buscar_por_cedula():
    # Verificar si el usuario está autenticado
    if 'username' not in session:
        flash('Por favor, inicia sesión primero.', 'warning')
        return redirect(url_for('login'))

    # Obtener el número de cédula del formulario
    cedula = request.args.get('cedula')

    # Conectar con la base de datos y buscar la solicitud por número de cédula
    conn = sqlite3.connect('solicitudes.db')
    c = conn.cursor()
    c.execute('SELECT * FROM usuarios WHERE numero_documento = ?', (cedula,))
    solicitud = c.fetchone()
    conn.close()

    if solicitud:
        # Si se encuentra una solicitud, redirigir a la página de detalles de solicitud
        return render_template('detalle_solicitud.html', solicitud=solicitud)
    else:
        # Si no se encuentra, mostrar un mensaje de error y redirigir a la página de administración
        flash('No se encontró ninguna solicitud con ese número de cédula.', 'warning')
        return redirect(url_for('admin'))

@app.route('/admin/eliminar/<int:id_solicitud>', methods=['GET'])
def eliminar_solicitud(id_solicitud):
    if 'username' not in session:
        flash('Por favor, inicia sesión primero.', 'warning')
        return redirect(url_for('login'))

    # Conectar a la base de datos y eliminar la solicitud
    conn = sqlite3.connect('solicitudes.db')
    c = conn.cursor()
    c.execute('DELETE FROM usuarios WHERE id = ?', (id_solicitud,))
    conn.commit()
    conn.close()
    
    flash('Solicitud eliminada exitosamente.', 'success')
    return redirect(url_for('admin'))



if __name__ == '__main__':
    app.run(debug=True, port=5001)

