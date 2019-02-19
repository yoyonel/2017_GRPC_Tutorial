# coding=utf-8
"""
TODO: refactorer pour séparer la définition des modèles et la gestion de l'ORM (sqlalchemy)
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from geoalchemy2 import Geometry
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    "postgresql://{PG_USER}:{PG_PASSWD}@{PG_HOST}:{PG_PORT}/{PG_DB}".format(
        PG_USER=os.environ.get("TUTORIAL_GRPC_PG_USER", 'docker'),
        PG_PASSWD=os.environ.get("TUTORIAL_GRPC_PG_PASSWD", 'docker'),
        PG_HOST=os.environ.get("TUTORIAL_GRPC_PG_HOST", 'localhost'),
        PG_PORT=int(os.getenv("TUTORIAL_GRPC_PG_PORT", "5432")),
        PG_DB=os.environ.get("TUTORIAL_GRPC_PG_DB", 'test'),
    ),
    echo=True
)
Base = declarative_base()


class Thing(Base):
    __tablename__ = "thing"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    geom = Column(Geometry('POLYGON'))


Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)
