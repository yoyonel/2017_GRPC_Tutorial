"""
"""
import logging
from sqlalchemy import func
from sqlalchemy.orm.query import Query
import statsd
from typing import Callable, List

from tutorial.grpc.geodatas.common.base import session_factory
from tutorial.grpc.geodatas.models.ogrgeojson import OGRGeoJSON
from tutorial.grpc.geodatas.models.thing import Thing
from tutorial.grpc.geodatas.proto import search_pb2, search_pb2_grpc
from tutorial.grpc.geodatas.tools.geometry import Position

logger = logging.getLogger(__name__)


def _query_to_responses(
        query: Query,
        func_response: Callable[[Query], str]
) -> List[search_pb2.SearchResponse]:
    """

    :param query:
    :param func_response:
    :return:
    """
    return [search_pb2.SearchResponse(response=func_response(rec))
            for rec in query]


def _search_thing(lat: float, lng: float, srid: int = -1) -> List[search_pb2.SearchResponse]:
    """

    :param lat:
    :param lng:
    :param srid:
    :return:
    """
    session = session_factory()
    query = session.query(Thing).filter(
        func.ST_Contains(Thing.geom,
                         Position(lat, lng, srid).to_wktelement))
    return _query_to_responses(query, lambda rec: rec.name)


def _search_commune(lat: float, lng: float, srid: int = 4326) -> List[search_pb2.SearchResponse]:
    """

    :param lat:
    :param lng:
    :param srid:
    :return:
    """
    session = session_factory()
    query = session.query(OGRGeoJSON).filter(
        func.ST_Contains(OGRGeoJSON.wkb_geometry,
                         Position(lat, lng, srid).to_wkbelement))
    return _query_to_responses(
        query,
        lambda rec: "{} - {} - {}".format(rec.insee, rec.nom, rec.wikipedia)
    )


class SearchServicer(search_pb2_grpc.SearchServicer):
    stat = statsd.StatsClient('localhost', 8125)

    @stat.timer("search")
    def search(self, request: search_pb2.SearchRequest, _context) -> search_pb2.SearchResponses:
        """

        :param request:
        :param _context:
        :return:
        """
        self.stat.incr("search_count")
        logger.info("search (commune) request: " + str(request))

        responses = _search_commune(request.lat, request.lng)

        logger.info("search responses: " + str(responses))
        return search_pb2.SearchResponses(responses=responses)

    @stat.timer("search_thing")
    def search_thing(self, request: search_pb2.SearchRequest, _context) -> search_pb2.SearchResponses:
        """

        :param request:
        :param _context:
        :return:
        """
        self.stat.incr("search_count")
        logger.info("search (thing) request: " + str(request))

        responses = _search_thing(request.lat, request.lng)

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
