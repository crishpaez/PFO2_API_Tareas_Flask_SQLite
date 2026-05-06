# PFO 2 - Sistema de Gestión de Tareas con API y Base de Datos

## Descripción

En este proyecto implementamos una API REST básica utilizando Flask y SQLite.

La aplicación nos permite:

- Registrar usuarios.
- Guardar contraseñas hasheadas.
- Iniciar sesión.
- Acceder a una ruta protegida `/tareas`.
- Probar la API mediante un cliente de consola.

El objetivo de este trabajo es aplicar conceptos de Programación sobre Redes, APIs REST, autenticación básica, persistencia de datos y seguridad en el manejo de contraseñas.

---

## Tecnologías utilizadas

- Python 3
- Flask
- SQLite
- Werkzeug Security
- Requests

---

## Estructura del proyecto

```text
PFO2_API_Tareas_Flask_SQLite/
│
├── servidor.py
├── cliente.py
├── requirements.txt
├── README.md
├── index.html
└── .gitignore

```

---

## Instrucciones para ejecutar el proyecto

### 1. Clonar el repositorio

```bash
git clone https://github.com/crishpaez/PFO2_API_Tareas_Flask_SQLite.git
```

### 2. Ingresar a la carpeta del proyecto

```bash
cd PFO2_API_Tareas_Flask_SQLite
```

### 3. Crear un entorno virtual

```bash
python -m venv venv
```

### 4. Activar el entorno virtual

En Windows:

```bash
venv\Scripts\activate
```

### 5. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 6. Ejecutar el servidor Flask

```bash
python servidor.py
```

El servidor quedará disponible en:

```text
http://127.0.0.1:5000
```

---

## Instrucciones para probar el proyecto

Una vez que el servidor esté en ejecución, se debe abrir otra terminal en la misma carpeta del proyecto y activar nuevamente el entorno virtual:

```bash
venv\Scripts\activate
```

Luego se ejecuta el cliente de consola:

```bash
python cliente.py
```

Desde el menú del cliente se pueden realizar las siguientes pruebas:

1. Registrar un usuario.
2. Iniciar sesión con el usuario registrado.
3. Acceder al endpoint `/tareas`.
4. Cerrar sesión.

---

## Flujo de prueba recomendado

### 1. Registrar usuario

Seleccionar la opción:

```text
1. Registrar usuario
```

Ejemplo de datos:

```text
Usuario: admin
Contraseña: admin
```

Respuesta esperada:

```json
{
  "mensaje": "Usuario registrado correctamente"
}
```

---

### 2. Iniciar sesión

Seleccionar la opción:

```text
2. Iniciar sesión
```

Ingresar el mismo usuario y contraseña registrados previamente.

Respuesta esperada:

```json
{
  "mensaje": "Inicio de sesión correcto",
  "usuario": "admin"
}
```

---

### 3. Ver tareas

Seleccionar la opción:

```text
3. Ver tareas
```

Respuesta esperada:

```html
<h1>Bienvenido, admin</h1>
<p>Accediste correctamente al sistema de gestión de tareas.</p>
<p>Esta sección representa el endpoint protegido GET /tareas.</p>
```

---

### 4. Cerrar sesión

Seleccionar la opción:

```text
4. Cerrar sesión
```

Respuesta esperada:

```json
{
  "mensaje": "Sesión cerrada correctamente"
}
```

---

## Endpoints principales

| Método | Endpoint | Descripción |
|---|---|---|
| POST | `/registro` | Registra un nuevo usuario con contraseña hasheada |
| POST | `/login` | Verifica las credenciales del usuario |
| GET | `/tareas` | Muestra un HTML de bienvenida si el usuario inició sesión |
| POST | `/logout` | Cierra la sesión del usuario |

---

## Base de datos

Al ejecutar el servidor, se crea automáticamente el archivo:

```text
tareas.db
```

La base de datos contiene la tabla `usuarios`, donde se almacenan los usuarios registrados.

La contraseña no se guarda en texto plano, sino como un hash en la columna:

```text
contrasena_hash
```

Un ejemplo de contraseña hasheada puede verse así:

```text
scrypt:32768:8:1$...
```

Esto confirma que el sistema protege las contraseñas mediante hashing y no almacena las claves reales de los usuarios.

---

## Nota sobre GitHub Pages

El proyecto incluye un archivo `index.html` para publicar una página informativa mediante GitHub Pages.

GitHub Pages muestra una presentación estática del proyecto, pero no ejecuta el servidor Flask ni la base de datos SQLite.  
Para probar la API, se debe ejecutar localmente el archivo:

```bash
python servidor.py
```

---

## Enlaces

GitHub Pages:  
https://crishpaez.github.io/PFO2_API_Tareas_Flask_SQLite/

---

## Autor

Humberto Cristian Páez