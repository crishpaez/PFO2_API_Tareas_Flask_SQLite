import sqlite3
from flask import Flask, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = "clave_secreta_pfo2"

BBDD_NAME = "tareas.db"


def obtenerConexion():
    # Abrimos conexión con la BBDD SQLite
    conexion = sqlite3.connect(BBDD_NAME)
    conexion.row_factory = sqlite3.Row
    return conexion


def inicializarBBDD():
    # Creamos las tablas necesarias si no existen
    try:
        conexion = obtenerConexion()
        cursor = conexion.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT NOT NULL UNIQUE,
                contrasena_hash TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tareas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                descripcion TEXT,
                estado TEXT DEFAULT 'pendiente',
                usuario_id INTEGER NOT NULL,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            )
        """)

        conexion.commit()
        conexion.close()
        print("[DB] Base de datos inicializada correctamente")

    except sqlite3.Error as e:
        print(f"[ERROR DB] No se pudo inicializar la base de datos: {e}")
        raise


@app.route("/")
def inicio():
    return """
    <html>
        <head>
            <title>PFO 2 - API de Tareas</title>
        </head>
        <body>
            <h1>PFO 2 - Sistema de Gestión de Tareas</h1>
            <p>API Flask funcionando correctamente.</p>
            <ul>
                <li>POST /registro</li>
                <li>POST /login</li>
                <li>GET /tareas</li>
            </ul>
        </body>
    </html>
    """


@app.route("/registro", methods=["POST"])
def registro():
    # Recibimos usuario y contraseña en formato JSON
    datos = request.get_json()

    if not datos:
        return jsonify({"error": "Debe enviar datos en formato JSON"}), 400

    usuario = datos.get("usuario")
    contrasena = datos.get("contraseña")

    if not usuario or not contrasena:
        return jsonify({"error": "Debe enviar usuario y contraseña"}), 400

    # Hasheamos la contraseña antes de guardarla
    contrasenaHash = generate_password_hash(contrasena)

    try:
        conexion = obtenerConexion()
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO usuarios (usuario, contrasena_hash)
            VALUES (?, ?)
        """, (usuario, contrasenaHash))

        conexion.commit()
        conexion.close()

        return jsonify({"mensaje": "Usuario registrado correctamente"}), 201

    except sqlite3.IntegrityError:
        return jsonify({"error": "El usuario ya existe"}), 409

    except sqlite3.Error as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500


@app.route("/login", methods=["POST"])
def login():
    # Verificamos las credenciales del usuario
    datos = request.get_json()

    if not datos:
        return jsonify({"error": "Debe enviar datos en formato JSON"}), 400

    usuario = datos.get("usuario")
    contrasena = datos.get("contraseña")

    if not usuario or not contrasena:
        return jsonify({"error": "Debe enviar usuario y contraseña"}), 400

    try:
        conexion = obtenerConexion()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT id, usuario, contrasena_hash
            FROM usuarios
            WHERE usuario = ?
        """, (usuario,))

        usuarioEncontrado = cursor.fetchone()
        conexion.close()

        if usuarioEncontrado is None:
            return jsonify({"error": "Credenciales incorrectas"}), 401

        # Verificamos la contraseña ingresada contra el hash guardado
        if not check_password_hash(usuarioEncontrado["contrasena_hash"], contrasena):
            return jsonify({"error": "Credenciales incorrectas"}), 401

        # Guardamos datos básicos en sesión
        session["usuario_id"] = usuarioEncontrado["id"]
        session["usuario"] = usuarioEncontrado["usuario"]

        return jsonify({
            "mensaje": "Inicio de sesión correcto",
            "usuario": usuarioEncontrado["usuario"]
        }), 200

    except sqlite3.Error as e:
        return jsonify({"error": f"Error en la base de datos: {e}"}), 500


@app.route("/tareas", methods=["GET"])
def tareas():
    # Ruta protegida: solo podemos acceder si el usuario ha iniciado sesión
    if "usuario" not in session:
        return """
        <html>
            <body>
                <h1>Acceso denegado</h1>
                <p>Debe iniciar sesión para ver las tareas.</p>
            </body>
        </html>
        """, 401

    usuario = session["usuario"]

    return f"""
    <html>
        <head>
            <title>Tareas</title>
        </head>
        <body>
            <h1>Bienvenido, {usuario}</h1>
            <p>Accediste correctamente al sistema de gestión de tareas.</p>
            <p>Esta sección representa el endpoint protegido GET /tareas.</p>
        </body>
    </html>
    """


@app.route("/logout", methods=["POST"])
def logout():
    # Cerramos la sesión del usuario
    session.clear()
    return jsonify({"mensaje": "Sesión cerrada correctamente"}), 200


if __name__ == "__main__":
    inicializarBBDD()
    app.run(debug=True)