import argparse
import sys

from src.database import crear_motor, crear_sesion, init_db
from src.seed import poblar_datos_demo


def main():
    parser = argparse.ArgumentParser(description="Gestión de Arriendo de Equipamiento Deportivo")
    parser.add_argument("--demo", action="store_true",
                        help="cargar datos de ejemplo si la base de datos está vacía")
    args = parser.parse_args()

    motor = crear_motor()
    init_db(motor)
    session = crear_sesion(motor)

    if args.demo:
        cargados = poblar_datos_demo(session)
        print("Datos de demostración cargados." if cargados else "La base ya tiene datos; no se cargó la demo.")

    try:
        from src.ui.app_window import VentanaPrincipal
    except ImportError as error:
        print(f"No se pudo cargar la interfaz gráfica: {error}")
        print("En Linux instala Tkinter con:  sudo apt install python3-tk")
        sys.exit(1)

    ventana = VentanaPrincipal(session)
    ventana.mainloop()
    session.close()


if __name__ == "__main__":
    main()