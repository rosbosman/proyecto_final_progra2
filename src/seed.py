from sqlalchemy import func, select

from src import services
from src.models import Categoria


def poblar_datos_demo(session) -> bool:
    """Carga datos de ejemplo. Devuelve False si la base ya tenía datos (no toca nada)."""
    if session.scalar(select(func.count(Categoria.id))):
        return False

    balon = services.crear_categoria(session, "Deportes de balón", "Fútbol, básquetbol, vóleibol")
    agua = services.crear_categoria(session, "Deportes acuáticos", "Paddle surf, kayak")
    montana = services.crear_categoria(session, "Montaña y outdoor", "Camping y trekking")
    combate = services.crear_categoria(session, "Deportes de combate", "Judo, jiu-jitsu, MMA, karate y esgrima")

    futbol = services.crear_equipo(session, "BALON", "Balón de fútbol N°5", balon.id, 2500, 12)
    basquet = services.crear_equipo(session, "BALON", "Balón de básquetbol", balon.id, 2500, 8)
    paddle = services.crear_equipo(session, "ACUATICO", "Tabla de paddle surf", agua.id, 12000, 4)
    kayak = services.crear_equipo(session, "ACUATICO", "Kayak individual", agua.id, 15000, 3)
    carpa = services.crear_equipo(session, "MONTANA", "Carpa 4 personas", montana.id, 9000, 5)
    mochila = services.crear_equipo(session, "MONTANA", "Mochila trekking 60L", montana.id, 5000, 6)
    kimono = services.crear_equipo(session, "COMBATE", "Kimono de judo", combate.id, 10000, 6)
    careta = services.crear_equipo(session, "COMBATE", "Careta de esgrima", combate.id, 6000, 5)

    ana = services.crear_cliente(session, "Ana Pérez", "ana.perez@correo.cl", "+56 9 1111 1111")
    luis = services.crear_cliente(session, "Luis Soto", "luis.soto@correo.cl", "+56 9 2222 2222")
    marta = services.crear_cliente(session, "Marta Rojas", "marta.rojas@correo.cl", "+56 9 3333 3333")
    pedro = services.crear_cliente(session, "Pedro Díaz", "pedro.diaz@correo.cl", "+56 9 4444 4444")

    # (equipo, cliente, inicio, fin, cantidad, devuelto?)
    arriendos = [
        (futbol, ana, "2026-11-02", "2026-11-04", 3, True),
        (futbol, luis, "2026-11-05", "2026-11-06", 2, True),
        (futbol, marta, "2026-11-12", "2026-11-14", 4, False),
        (kimono, pedro, "2026-11-03", "2026-11-05", 2, True),
        (kimono, ana, "2026-11-10", "2026-11-12", 1, True),
        (kimono, luis, "2026-11-16", "2026-11-20", 2, False),
        (carpa, marta, "2026-11-07", "2026-11-10", 2, True),
        (carpa, pedro, "2026-11-14", "2026-11-18", 1, False),
        (kayak, ana, "2026-11-08", "2026-11-09", 1, True),
        (paddle, luis, "2026-11-15", "2026-11-17", 2, False),
        (mochila, marta, "2026-11-01", "2026-11-03", 3, True),
        (basquet, pedro, "2026-11-11", "2026-11-13", 2, True),
        (careta, ana, "2026-11-17", "2026-11-19", 2, False),
    ]
    for equipo, cliente, inicio, fin, cantidad, devuelto in arriendos:
        arriendo = services.registrar_arriendo(session, equipo.id, cliente.id, inicio, fin, cantidad)
        if devuelto:
            services.registrar_devolucion(session, arriendo.id)
    return True


if __name__ == "__main__":
    from src.database import crear_motor, crear_sesion, init_db

    motor = crear_motor()
    init_db(motor)
    with crear_sesion(motor) as sesion:
        print("Datos de demo cargados." if poblar_datos_demo(sesion) else "La base ya tenía datos.")