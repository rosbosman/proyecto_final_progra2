from abc import ABC, abstractmethod

from src.models import (
    Equipo,
    EquipoAcuatico,
    EquipoBalon,
    EquipoMontana,
    EquipoCombate,
)


class EquipoCreator(ABC):
    """Creator: declara el factory method y la lógica común de creación."""

    @abstractmethod
    def factory_method(self) -> type[Equipo]:
        """Devuelve la clase concreta de equipo que este creador fabrica."""

    def crear_equipo(self, nombre, categoria_id, precio_diario, stock_total) -> Equipo:
        clase_equipo = self.factory_method()
        return clase_equipo(
            nombre=nombre,
            categoria_id=categoria_id,
            precio_diario=precio_diario,
            stock_total=stock_total,
            stock_disponible=stock_total,  # al crearlo, todo el stock está disponible
        )


class EquipoGenericoCreator(EquipoCreator):
    def factory_method(self):
        return Equipo


class EquipoBalonCreator(EquipoCreator):
    def factory_method(self):
        return EquipoBalon


class EquipoAcuaticoCreator(EquipoCreator):
    def factory_method(self):
        return EquipoAcuatico


class EquipoMontanaCreator(EquipoCreator):
    def factory_method(self):
        return EquipoMontana


class EquipoCombateCreator(EquipoCreator):
    def factory_method(self):
        return EquipoCombate


# Registro clave de tipo -> creador. Es lo único que la interfaz y los servicios consultan.
CREADORES: dict[str, EquipoCreator] = {
    "GENERICO": EquipoGenericoCreator(),
    "BALON": EquipoBalonCreator(),
    "ACUATICO": EquipoAcuaticoCreator(),
    "MONTANA": EquipoMontanaCreator(),
    "COMBATE": EquipoCombateCreator(),
}


def obtener_creador(tipo: str) -> EquipoCreator:
    try:
        return CREADORES[tipo]
    except KeyError:
        raise ValueError(f"Tipo de equipo desconocido: {tipo!r}") from None


def tipos_disponibles() -> list[tuple[str, str]]:
    """Lista (clave, etiqueta legible) para mostrar en la interfaz."""
    return [(clave, creador.factory_method().ETIQUETA) for clave, creador in CREADORES.items()]