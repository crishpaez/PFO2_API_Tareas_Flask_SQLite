import requests

BASE_URL = "http://127.0.0.1:5000"


def mostrarMenu():
    print("\n=== Cliente PFO 2 ===")
    print("1. Registrar usuario")
    print("2. Iniciar sesión")
    print("3. Ver tareas")
    print("4. Cerrar sesión")
    print("5. Salir")


def registrarUsuario(sesion):
    usuario = input("Usuario: ")
    contrasena = input("Contraseña: ")

    respuesta = sesion.post(
        f"{BASE_URL}/registro",
        json={
            "usuario": usuario,
            "contraseña": contrasena
        }
    )

    print("Estado:", respuesta.status_code)
    print("Respuesta:", respuesta.text)


def iniciarSesion(sesion):
    usuario = input("Usuario: ")
    contrasena = input("Contraseña: ")

    respuesta = sesion.post(
        f"{BASE_URL}/login",
        json={
            "usuario": usuario,
            "contraseña": contrasena
        }
    )

    print("Estado:", respuesta.status_code)
    print("Respuesta:", respuesta.text)


def verTareas(sesion):
    respuesta = sesion.get(f"{BASE_URL}/tareas")

    print("Estado:", respuesta.status_code)
    print("Respuesta del servidor:")
    print(respuesta.text)


def cerrarSesion(sesion):
    respuesta = sesion.post(f"{BASE_URL}/logout")

    print("Estado:", respuesta.status_code)
    print("Respuesta:", respuesta.text)


def main():
    sesion = requests.Session()

    while True:
        mostrarMenu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrarUsuario(sesion)
        elif opcion == "2":
            iniciarSesion(sesion)
        elif opcion == "3":
            verTareas(sesion)
        elif opcion == "4":
            cerrarSesion(sesion)
        elif opcion == "5":
            print("Finalizando cliente...")
            break
        else:
            print("Opción inválida")


if __name__ == "__main__":
    main()