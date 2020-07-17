# -*- coding: utf-8 -*-
"""Settings del proyecto."""

from pathlib import Path

from petri.loggin import LogFormatter
from petri.loggin import LogLevel
from petri.settings import BaseSettings


class Settings(BaseSettings):
    """Configuraciones comumnes."""

    SQLALCHEMY_DATABASE_URI: str
    """Conexión a la base de datos de redes sociales"""


class Production(Settings):
    """Configuraciones ambiente de producción."""

    LOG_FORMAT = LogFormatter.JSON
    LOG_LEVEL = LogLevel.TRACE


class Development(Settings):
    """Configuraciones ambiente de desarrollo."""

    LOG_FORMAT = LogFormatter.COLOR  # requires colorama
    LOG_LEVEL = LogLevel.INFO
