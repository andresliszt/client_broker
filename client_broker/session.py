# -*- coding: utf-8 -*-
"""Configuración de conexión y manejo de sesiones."""
from contextlib import contextmanager
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm import sessionmaker

from client_broker import SETTINGS

ENGINE: Engine = create_engine(SETTINGS.SQLALCHEMY_DATABASE_URI)
"""Establece la conexión la db dada por la connection string"""

@contextmanager
def session_scope(engine: Any = ENGINE):
    """Transaccional manejo de las sessiones."""

    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        yield session

    except DatabaseError:
        session.rollback()
        raise

    finally:
        session.close()
