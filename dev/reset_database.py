#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import logging
import os

from sqlalchemy.sql import text

import db
import settings
from db.models import SQLAlchemyBase, User, GenreEnum, UserToken, RolEnum, AssociationUserInstruments
from db.models import Instruments, MusicalGenere
from settings import DEFAULT_LANGUAGE

# LOGGING
mylogger = logging.getLogger(__name__)
settings.configure_logging()


def execute_sql_file(sql_file):
    sql_folder_path = os.path.join(os.path.dirname(__file__), "sql")
    sql_file_path = open(os.path.join(sql_folder_path, sql_file), encoding="utf-8")
    sql_command = text(sql_file_path.read())
    db_session.execute(sql_command)
    db_session.commit()
    sql_file_path.close()


if __name__ == "__main__":
    settings.configure_logging()

    db_session = db.create_db_session()

    # -------------------- REMOVE AND CREATE TABLES --------------------
    mylogger.info("Removing database...")
    SQLAlchemyBase.metadata.drop_all(db.DB_ENGINE)
    mylogger.info("Creating database...")
    SQLAlchemyBase.metadata.create_all(db.DB_ENGINE)

    # -------------------- CREATE USERS --------------------
    mylogger.info("Creating default users...")
    # noinspection PyArgumentList
    user_admin = User(
        created_at=datetime.datetime(2020, 1, 1, 0, 1, 1),
        username="admin",
        email="admin@damcore.com",
        name="Administrator",
        surname="DamCore",
        genere=GenreEnum.male,
        gps="42.090205,1.1504",
        rol=RolEnum.sponsor,
        gen_exp=4.5,
        description="description admin"
    )
    user_admin.set_password("DAMCoure")


    # -------------------- CREATE Instruments --------------------
    mylogger.info("Creating instrumets data...")
    # noinspection PyArgumentList
    instrument1 = Instruments(
        name="Guitarra"
    )
    instrument2 = Instruments(
        name="Trompeta"
    )
    instrument3 = Instruments(
        name="Piano"
    )
    instrument4 = Instruments(
        name="Maracas"
    )
    # -------------------- CREATE Generes --------------------

    mylogger.info("CreatinMusicalGenere data...")
    genere1 = MusicalGenere(
        name="Rock"
    )
    genere2 = MusicalGenere(
        name="Pop"
    )
    genere3 = MusicalGenere(
        name="Country"
    )
    genere4 = MusicalGenere(
        name="Metal"
    )


    usuariadmin_guitarra = AssociationUserInstruments(
        id_user=1,
        id_instrument=1,
        expirience=4
    )
    usuari1_guitarra = AssociationUserInstruments(
        id_user=2,
        id_instrument=1,
        expirience=4
    )
    usuari2_guitarra = AssociationUserInstruments(
        id_user=3,
        id_instrument=1,
        expirience=4
    )
    usuari1_piano = AssociationUserInstruments(
        id_user=2,
        id_instrument=3,
        expirience=2
    )

    # noinspection PyArgumentList
    user_1 = User(
        created_at=datetime.datetime(2020, 1, 1, 0, 1, 1),
        username="34938030161",
        email="usuari1@gmail.com",
        name="usuari",
        surname="1",
        rol=RolEnum.user,
        birthdate=datetime.datetime(1989, 1, 1),
        genere=GenreEnum.male,
        gps="42.390205,3.1504",
        description="description user1",
        firstTime=False,
        gen_exp=3.0,
        user_musicalgeneres=[genere1, genere2]
    )
    user_1.set_password("1234")
    user_1.tokens.append(UserToken(token="656e50e154865a5dc469b80437ed2f963b8f58c8857b66c9bf"))

    # noinspection PyArgumentList
    user_2 = User(
        created_at=datetime.datetime(2020, 1, 1, 0, 1, 1),
        username="user2",
        email="user2@gmail.com",
        name="user",
        surname="2",
        birthdate=datetime.datetime(2017, 1, 1),
        genere=GenreEnum.male,
        gps="40.390205,2.5504",
        description="description user2",
        gen_exp=5.0,
        user_musicalgeneres=[genere4,genere2]
    )
    user_2.set_password("r45tgt")
    user_2.tokens.append(UserToken(token="0a821f8ce58965eadc5ef884cf6f7ad99e0e7f58f429f584b2"))

    user_1.subscribed_to.append(user_2)
    user_admin.subscribed_to.append(user_1)

    # ----Adding Generes----#
    db_session.add(genere1)
    db_session.add(genere2)
    db_session.add(genere3)
    db_session.add(genere4)

    # ----Adding Users----#
    db_session.add(user_admin)
    db_session.add(user_1)
    db_session.add(user_2)

    #----Adding Instruments----#
    db_session.add(instrument1)
    db_session.add(instrument2)
    db_session.add(instrument3)
    db_session.add(instrument4)

    db_session.add(usuari1_guitarra)
    db_session.add(usuari2_guitarra)

    db_session.add(usuari1_piano)
    db_session.add(usuariadmin_guitarra)

    db_session.commit()
    db_session.close()
