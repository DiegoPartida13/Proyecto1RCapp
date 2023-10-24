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
        return connection, cursor

    except Exception as e:
        print(f'Error al conectar a la base de datos: {e}')
        return None, None

# Recopila los valores de los campos del formulario de registro.html
form = cgi.FieldStorage()
nombres = form.getvalue('nombres')
apellidoPaterno = form.getvalue('apellido-paterno')
apellidoMaterno = form.getvalue('apellido-materno')
fechaNacimiento = form.getvalue('fecha-nacimiento')
correoElectronico = form.getvalue('correo-electronico')
contrasena = form.getvalue('contrasena')
confirmarContrasena = form.getvalue('confirmar-contrasena')
pais = form.getvalue('pais')

# Función para hashear la contraseña
def hashear_contrasena(contrasena):
    hash_obj = hashlib.sha256()
    hash_obj.update(contrasena.encode('utf-8'))
    contrasena_hasheada = hash_obj.hexdigest()
    return contrasena_hasheada

#Función para insertar un usuario en la base de datos
def registrar_usuario():
    connection, cursor = conectar_base_datos()
    if connection and cursor:
        try:
            contrasena_hasheada=hashear_contrasena(contrasena)
            sql = "INSERT INTO usuarios (nombres, apellido_paterno, apellido_materno, fecha_nacimiento, email, contrasena, pais) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (nombres, apellidoPaterno, apellidoMaterno, fechaNacimiento, correoElectronico, contrasena_hasheada, pais))
            
            # Confirma la transacción y cierra la conexión
            connection.commit()
            cursor.close()
            connection.close()
            print('Usuario insertado exitosamente!')

        except Exception as e:
            print(f'Error al insertar el usuario en la base de datos: {e}')

# Ejecutamos la función
registrar_usuario()
