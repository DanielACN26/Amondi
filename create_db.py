import sqlite3

# Conectar a la base de datos (se creará el archivo si no existe)
conn = sqlite3.connect('solicitudes.db')
c = conn.cursor()

# Crear la tabla 'usuarios' en la base de datos
c.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombres_apellidos TEXT,
        alias TEXT,
        genero TEXT,
        zona_residencia TEXT,
        estado TEXT,
        urbanizacion TEXT,
        tipo_documento TEXT,
        numero_documento TEXT,
        numero_principal TEXT,
        numero_secundario TEXT,
        correo TEXT,
        nombre_emprendimiento TEXT,
        instagram_emprendimiento TEXT,
        referido_nombre TEXT,
        referido_telefono TEXT
    )
''')

# Guardar los cambios y cerrar la conexión
conn.commit()
conn.close()
