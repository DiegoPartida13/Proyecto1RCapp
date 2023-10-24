#!/usr/bin/python3
import cgi
import cgitb
import psycopg2
import hashlib

# Activa la depuración de errores para ver posibles problemas en el navegador
cgitb.enable()

# Imprime las cabeceras HTTP
print("Content-Type: text/html")
print()

# Función para conectar a la base de datos
def conectar_base_datos():
    try:
        connection = psycopg2.connect(
            dbname='datosusuarios',
            user='redes',
            password='',
            host='172.16.0.4',
            port='5432'
        )
        cursor = connection.cursor()
        #print('Conexión exitosa a la base de datos')
        return connection, cursor

    except Exception as e:
        print(f'Error al conectar a la base de datos: {e}')
        return None, None

# Recopila los valores de los campos del formulario de inicio de sesión
form = cgi.FieldStorage()
correoElectronico = form.getvalue('correo-electronico')
contrasena = form.getvalue('contrasena')

# Función para hashear la contraseña
def hashear_contrasena(contrasena):
    hash_obj = hashlib.sha256()
    hash_obj.update(contrasena.encode('utf-8'))
    contrasena_hasheada = hash_obj.hexdigest()
    return contrasena_hasheada

# Función para verificar las credenciales del usuario
def verificar_credenciales(correo, contrasena):
    connection, cursor = conectar_base_datos()
    if connection and cursor:
        try:
            # Consulta la base de datos para el usuario con el correo proporcionado
            cursor.execute("SELECT id, contrasena FROM usuarios WHERE email = %s", (correo,))
            usuario = cursor.fetchone()

            if usuario and usuario[1] == hashear_contrasena(contrasena):
                # Las credenciales son válidas, retorna el ID del usuario
                return usuario[0]

        except Exception as e:
            print(f'Error al verificar las credenciales: {e}')

    return None

# Verifica las credenciales del usuario
usuario_id = verificar_credenciales(correoElectronico, contrasena)

if usuario_id:
    # Credenciales válidas, redirigir al "index.html"
    print("Content-Type: text/html")
    print()  # Línea en blanco
    print("<meta charset='UTF-8'>")
    print("<h1>Inicio de sesión exitoso.</h1>")
else:
    # Credenciales inválidas, muestra un mensaje de error u otra página
    print("Content-Type: text/html")
    print()  # Línea en blanco
    print("<meta charset='UTF-8'>")
    print("<p>Inicio de sesión fallido. Verifica tu correo y contraseña.</p>")
