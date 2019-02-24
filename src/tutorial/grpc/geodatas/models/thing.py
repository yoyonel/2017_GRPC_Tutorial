"""
"""
from sqlalchemy import Column, Integer, String
from geoalchemy2 import Geometry

from ..common.base import Base


class Thing(Base):
    __tablename__ = "thing"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    geom = Column(Geometry('POLYGON'))
