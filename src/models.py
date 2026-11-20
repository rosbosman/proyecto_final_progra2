from datetime import date

from sqlalchemy import CheckConstraint, Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base

ESTADO_ACTIVO = "ACTIVO"
ESTADO_DEVUELTO = "DEVUELTO"


class Categoria(Base):
    __tablename__ = "categorias"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(80), unique=True)
    descripcion: Mapped[str | None] = mapped_column(String(255), default="")

    equipos: Mapped[list["Equipo"]] = relationship(back_populates="categoria")

    def __repr__(self) -> str:
        return f"<Categoria {self.id} {self.nombre!r}>"


class Equipo(Base):
    __tablename__ = "equipos"
    __table_args__ = (
        CheckConstraint("precio_diario > 0", name="ck_equipo_precio_positivo"),
        CheckConstraint("stock_total >= 0", name="ck_equipo_stock_total_no_negativo"),
        CheckConstraint("stock_disponible >= 0", name="ck_equipo_stock_disp_no_negativo"),
        CheckConstraint("stock_disponible <= stock_total", name="ck_equipo_stock_disp_menor_total"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))
    tipo: Mapped[str] = mapped_column(String(20), default="GENERICO")
    categoria_id: Mapped[int] = mapped_column(ForeignKey("categorias.id", ondelete="RESTRICT"))
    precio_diario: Mapped[float] = mapped_column(Float)
    stock_total: Mapped[int] = mapped_column(Integer)
    stock_disponible: Mapped[int] = mapped_column(Integer)

    categoria: Mapped["Categoria"] = relationship(back_populates="equipos")
    arriendos: Mapped[list["Arriendo"]] = relationship(back_populates="equipo")

    __mapper_args__ = {
        "polymorphic_on": "tipo",
        "polymorphic_identity": "GENERICO",
    }

    ETIQUETA = "general"

    def recomendacion(self) -> str:
        return "revisar estado general del equipo antes de entregar"

    def __repr__(self) -> str:
        return (
            f"<{type(self).__name__} {self.id} {self.nombre!r} "
            f"disp={self.stock_disponible}/{self.stock_total}>"
        )


class EquipoBalon(Equipo):
    __mapper_args__ = {"polymorphic_identity": "BALON"}
    ETIQUETA = "deportes de balon"

    def recomendacion(self) -> str:
        return "verificar la presion de la pelota y que no tenga cortes ni que este deformada"


class EquipoAquatico(Equipo):
    __mapper_args__ = {"polymorphic_identity": "AQUATICO"}
    ETIQUETA = "deporte acuatico"

    def recomendacion(self) -> str:
        return "entregar chaleco salvavidas"


class EquipoMontana(Equipo):
    __mapper_args__ = {"polymorphic_identity": "MONTANA"}
    ETIQUETA = "montañismo y outdoor"

    def recomendacion(self) -> str:
        return "revisar equipamiento de montañismo"


class EquipoCombate(Equipo):
    __mapper_args__ = {"polymorphic_identity": "COMBATE"}
    ETIQUETA = "deporte de contacto"

    def recomendacion(self) -> str:
        return "revisar protecciones; entregar limpio y con todas las protecciones"


class Cliente(Base):
    __tablename__ = "clientes"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))
    correo: Mapped[str] = mapped_column(String(120), unique=True)
    telefono: Mapped[str | None] = mapped_column(String(30), default="")

    arriendos: Mapped[list["Arriendo"]] = relationship(back_populates="cliente")

    def __repr__(self) -> str:
        return f"<Cliente {self.id} {self.nombre!r}>"


class Arriendo(Base):
    __tablename__ = "arriendos"
    __table_args__ = (
        CheckConstraint("cantidad > 0", name="ck_arriendo_cantidad_positiva"),
        CheckConstraint("fecha_fin_prevista >= fecha_inicio", name="ck_arriendo_fechas"),
        CheckConstraint(
            f"estado IN ('{ESTADO_ACTIVO}', '{ESTADO_DEVUELTO}')",
            name="ck_arriendo_estado",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    equipo_id: Mapped[int] = mapped_column(ForeignKey("equipos.id", ondelete="RESTRICT"))
    cliente_id: Mapped[int] = mapped_column(ForeignKey("clientes.id", ondelete="RESTRICT"))
    fecha_inicio: Mapped[date] = mapped_column(Date)
    fecha_fin_prevista: Mapped[date] = mapped_column(Date)
    cantidad: Mapped[int] = mapped_column(Integer)
    estado: Mapped[str] = mapped_column(String(10), default=ESTADO_ACTIVO)
    fecha_devolucion: Mapped[date | None] = mapped_column(Date, default=None)

    equipo: Mapped["Equipo"] = relationship(back_populates="arriendos")
    cliente: Mapped["Cliente"] = relationship(back_populates="arriendos")

    def __repr__(self) -> str:
        return (
            f"<Arriendo {self.id} equipo={self.equipo_id} "
            f"cliente={self.cliente_id} {self.estado}>"
        )