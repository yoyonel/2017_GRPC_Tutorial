"""
"""
import logging
from sqlalchemy import func
import statsd

from tutorial.grpc.geodatas.common.base import session_factory
from tutorial.grpc.geodatas.models.ogrgeojson import OGRGeoJSON
from tutorial.grpc.geodatas.models.thing import Thing
from tutorial.grpc.geodatas.proto import search_pb2, search_pb2_grpc

logger = logging.getLogger(__name__)


def generate_pg_point(lat: int, lng: int, srid: int = 4326) -> str:
    """
    https://gis.stackexchange.com/questions/189987/casting-between-postgis-types-in-geoalchemy

    :param lat:
    :param lng:
    :param srid:
    :return:
    """
    return f"SRID={srid};POINT({lat} {lng})"


def _query_to_responses(query, func_response):
    """

    :param query:
    :param func_response:
    :return:
    """
    return [search_pb2.SearchResponse(response=func_response(rec))
            for rec in query]


def _search_thing(lat, lng):
    """

    :param lat:
    :param lng:
    :return:
    """
    session = session_factory()
    query = session.query(Thing).filter(
        func.ST_Contains(Thing.geom,
                         generate_pg_point(lat, lng)))
    return _query_to_responses(query, lambda rec: rec.name)


def _search_commune(lat, lng, srid=4326):
    """

    :param lat:
    :param lng:
    :param srid:
    :return:
    """
    session = session_factory()
    query = session.query(OGRGeoJSON).filter(
        func.ST_Contains(OGRGeoJSON.wkb_geometry,
                         generate_pg_point(lat, lng, srid)))
    return _query_to_responses(
        query,
        lambda rec: "{} - {} - {}".format(rec.insee, rec.nom, rec.wikipedia)
    )


class SearchServicer(search_pb2_grpc.SearchServicer):
    stat = statsd.StatsClient('localhost', 8125)

    @stat.timer("search")
    def search(self, request, _context):
        """

        :param request:
        :param _context:
        :return:
        """
        self.stat.incr("search_count")
        logger.info("search request: " + str(request))

        # responses = _search_thing(request.lat, request.lng)
        responses = _search_commune(request.lat, request.lng)

        logger.info("search responses: " + str(responses))
        return search_pb2.SearchResponses(responses=responses)

    @stat.timer("monitor")
    def monitor(self, _request, _context):
        """

        :param _request:
        :param _context:
        :return:
        """
        session = session_factory()
        self.stat.incr("monitor_count")
        n_things = session.query(Thing).count()
        return search_pb2.MonitorResponse(n_things=n_things)
