from pathlib import Path

from sqlalchemy import Engine, create_engine, event
from sqlalchemy.orm import DeclarativeBase, Session

RUTA_BD = Path(__file__).resolve().parent.parent / "data" / "arriendo_deportivo.db"


class Base(DeclarativeBase):
    pass


def _activar_foreign_keys(conexion_dbapi, _registro) -> None:
    cursor = conexion_dbapi.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    cursor.close()


def crear_motor(url: str | None = None) -> Engine:
    if url is None:
        RUTA_BD.parent.mkdir(parents=True, exist_ok=True)
        url = f"sqlite:///{RUTA_BD}"
    motor = create_engine(url)
    event.listen(motor, "connect", _activar_foreign_keys)
    return motor


def crear_session(motor: Engine) -> Session:
    return Session(motor)


def init_db(motor: Engine) -> None:
    from src import models  # noqa: F401

    Base.metadata.create_all(motor)