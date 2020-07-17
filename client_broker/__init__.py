# -*- coding: utf-8 -*-
"""Inicialización paquete."""

from petri import Petri

pkg = Petri(__file__)  # pylint: disable=invalid-name

SETTINGS = pkg.settings

logger = pkg.log

from client_broker.reflect_db import reflect_database

try:
    TABLES = reflect_database()

    RecintosSalud = TABLES["RecintosSalud"]

    RegistroRespiradoresMinsalActual = TABLES["RegistroRespiradoresMinsalActual"]

    RegistroRespiradoresMinsalTotal = TABLES["RegistroRespiradoresMinsalTotal"]

    MedicionesRespiradoresActual = TABLES["MedicionesRespiradoresActual"]

    MedicionesRespiradoresTotal = TABLES["MedicionesRespiradoresTotal"]

except KeyError:
    raise KeyError(
        "El esquema de base de datos no contiene una(s) de la(s) tablas(s) definidas"
    )
