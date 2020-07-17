# -*- coding: utf-8 -*-
"""Utilidades para guardado de data desde el cliente del broker"""
import json

from sqlalchemy.exc import IntegrityError
from client_broker.session import ENGINE

from client_broker import MedicionesRespiradoresActual, MedicionesRespiradoresTotal
from client_broker.session import session_scope


def insert_payload(payload: dict):
    """Inserta registro en la base de datos"""

    with session_scope() as sess:

        sess.add(MedicionesRespiradoresTotal(**payload))

        try:
            sess.add(MedicionesRespiradoresActual(**payload))
            sess.commit()

        except IntegrityError:

            sess.query(MedicionesRespiradoresActual).filter_by(
                id_controlador=payload["id_controlador"]
            ).update(values=payload)

        sess.add(MedicionesRespiradoresTotal(**payload))
        sess.commit()
