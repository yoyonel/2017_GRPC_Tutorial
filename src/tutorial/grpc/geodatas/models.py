from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from geoalchemy2 import Geometry
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    "postgresql://{PG_USER}:{PG_PASSWD}@{PG_HOST}:{PG_PORT}/{PG_DB}".format(
        PG_USER='docker',
        PG_PASSWD='docker',
        PG_HOST='localhost',
        PG_PORT='5432',
        PG_DB='test',
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
