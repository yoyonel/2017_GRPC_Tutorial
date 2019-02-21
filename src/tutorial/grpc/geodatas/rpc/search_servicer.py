"""

"""
import logging
from sqlalchemy import func
import statsd

from tutorial.grpc.geodatas.models.models import Thing, session
from tutorial.grpc.geodatas.proto import search_pb2, search_pb2_grpc


logger = logging.getLogger(__name__)


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
        query = session.query(Thing).filter(
            func.ST_Contains(Thing.geom, 'POINT({} {})'.format(request.lat, request.lng)))
        responses = [search_pb2.SearchResponse(
            response=rec.name) for rec in query]
        logger.info("search responses: " + str(responses))
        return search_pb2.SearchResponses(responses=responses)

    @stat.timer("monitor")
    def monitor(self, _request, _context):
        """

        :param _request:
        :param _context:
        :return:
        """
        self.stat.incr("monitor_count")
        n_things = session.query(Thing).count()
        return search_pb2.MonitorResponse(n_things=n_things)
