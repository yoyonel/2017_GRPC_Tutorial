"""
"""
from sqlalchemy import Table

from ..common.base import Base, engine


class OGRGeoJSON(Base):
    # https://docs.sqlalchemy.org/en/latest/core/reflection.html
    __table__ = Table('ogrgeojson', Base.metadata, autoload=True, autoload_with=engine)
