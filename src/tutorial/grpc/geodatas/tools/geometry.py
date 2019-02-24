"""
"""
from attr import dataclass
from geoalchemy2 import WKBElement, WKTElement
from geoalchemy2.shape import from_shape
from shapely.geometry import Point


@dataclass
class Position:
    lat: float
    lng: float
    srid: int = 4326

    @property
    def to_wktelement(self) -> WKTElement:
        """Generate WKTElement from position.

        https://geoalchemy-2.readthedocs.io/en/0.2.6/elements.html
        :return:
        """
        return WKTElement(f"POINT({self.lat} {self.lng})", srid=self.srid)

    @property
    def to_wkbelement(self) -> WKBElement:
        """Generate WKBElement from position.

        https://geoalchemy-2.readthedocs.io/en/0.2.6/shape.html#geoalchemy2.shape.from_shape
        """
        return from_shape(Point(self.lat, self.lng), srid=self.srid)
