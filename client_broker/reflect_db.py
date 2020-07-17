'''Reflexión base de datos

En este modulo se refleja el esquema de base de datos para 
los respiradores.El schema debió ser creado en un servidor de 
base de datos, postgres en primera instancia. 
Lo que hacemos aquí es pasar dicho esquema a un 
Object Relational Mapper(ORM) para poder hacer queries a través de
sqlachemy. El esquema de respiradores, esta construido en el paquete
de python que disponibiliza la aplicación que lee los datos de los
respiradores. El esmquema de base de datos es el siguiente:

class RecintosSalud(Base):
    """Tabla conteniendo la información de los recintos de salud."""

    codigo_establecimiento = Column(Integer, primary_key=True, unique=True)
    """Identificador único del recinto de salud"""

    codigo_region = Column(Integer)
    """Identificador de región"""

    region = Column(String())
    """Nombre de la región"""

    seremi_servicio_salud = Column(String())

    tipo_establecimiento = Column(String())
    """Tipo de establecimiento (Hostpital, clínica, etc)"""
    # TODO: HACER UN ENUM??

    nombre_recinto = Column(String())
    """Nombre oficial del establecimiento"""

    codigo_comuna = Column(String())
    """Código de la comuna"""

    comuna = Column(String())
    """Nombre de la comuna"""

    via = Column(String())

    direccion_numero = Column(Integer)

    direccion_calle = Column(String())

    latitud = Column(Float)

    longitud = Column(Float)

    @hybrid_property
    def direccion_completa(self):
        return (
            self.via
            + " "
            + self.direccion_calle
            + " "
            + self.direccion_numero
            + ", "
            + self.comuna
            + ", "
            + self.region
        )


class RegistroRespiradoresMinsalMixing:
    """Clase Mixing para Registro distribución respiradores del Minsal."""

    nombre_recinto = Column(String(), nullable=False)
    """Nombre del recinto donde fue enviado dicho controlador"""

    @declared_attr
    def codigo_establecimiento(self):
        """Código del establecimiento de destinto."""
        return Column(
            Integer, ForeignKey("RecintosSalud.codigo_establecimiento"), nullable=False,
        )

    @declared_attr
    def codigo_region(self):
        """Código de la región de desintino."""
        return Column(
            Integer, ForeignKey("RecintosSalud.codigo_region"), nullable=False
        )

    @declared_attr
    def codigo_comuna(self):
        """Código de la comuna de desintino."""
        return Column(
            String(), ForeignKey("RecintosSalud.codigo_region"), nullable=False
        )

    latitud = Column(Float , nullable = False)
    """Latitud geográfica del lugar de destino"""

    longitud = Column(Float, nullable = False)
    """Longitud geográfica del lugar de destino"""

    fecha_envio = Column(DateTime)
    """Fecha en que fue/será despachado el respirador/controlador"""


class MedicionesRespiradoresMixing:
    """Clase mixing para las mediciones de respiradores."""

    # TODO: SETEAR LA FECHA DE MANERA AUTOMÁTICA

    nombre_recinto = Column(String())
    """Nombre del recinto donde fue enviado dicho controlador"""

    latitud = Column(Float)
    """Latitud geográfica que registra el controlador"""

    longitud = Column(Float)
    """Longitud geográfica que registra el controlador"""

    latitud_wifi = Column(Float)
    """Latitud geográfica que registra el wifi del controlador"""
   
    longitud_wifi = Column(Float)
    """Longitud geográfica que registra el wifi del controlador"""

    estado = Column(Boolean)
    """Estado del respirador, 0 es apagado y 1 encendido"""

    amperage = Column(Float)
    """Magnitud del amperage que registra el controlador"""

    fecha = Column(DateTime, nullable=False)
    """Fecha de medición"""

    wifi = Column(String())
    """Nombre de la señal de wifi del controlador"""

    ip_cliente = Column(String())

    ip_publica = Column(String())

    mac = Column(String())


class RegistroRespiradoresMinsalActual(RegistroRespiradoresMinsalMixing, Base):

    id_controlador = Column(BIGINT, primary_key=True, unique=True)
    """Identificador único del controlador"""


class RegistroRespiradoresMinsalTotal(RegistroRespiradoresMinsalMixing, Base):

    id = Column(BIGINT, primary_key=True, autoincrement=True)

    id_controlador = Column(BIGINT, nullable=False)
    """Identificador único del controlador"""


class MedicionesRespiradoresTotal(MedicionesRespiradoresMixing, Base):

    # TODO: SETEAR LA FECHA DE MANERA AUTOMÁTICA

    """En esta tabla se guardará todo el registro de los controladores.

    Servirá para entregar informes de la variación en el tiempo del
    estado de los respiradores distribuidos.

    """

    id = Column(Integer, primary_key=True, autoincrement=True)

    id_controlador = Column(BIGINT)


class MedicionesRespiradoresActual(MedicionesRespiradoresMixing, Base):

    """En esta tabla se guardará todo el último registro de medición.

    Servirá para entregar resultados de consulta de estado actual de

    los respiradores distribuidos

    """

    id_controlador = Column(BIGINT, primary_key=True, unique=True)
'''
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base

from client_broker.session import ENGINE


def reflect_database(engine=ENGINE):
    """Refleja schema de base de datos en ORM"""

    Base = declarative_base()
    metadata = MetaData(bind=engine)
    Base.metadata = metadata
    metadata.reflect()
    tables_dict = {}

    for tablename, tableobj in metadata.tables.items():
        tables_dict[tablename] = type(str(tablename), (Base,), {"__table__": tableobj})

    return tables_dict
