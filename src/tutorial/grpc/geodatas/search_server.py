import sys
import consul
import logging
import statsd
import random
from concurrent import futures
import grpc
from sqlalchemy import func
import signal
import pkg_resources

from tutorial.grpc.geodatas.models import session, Thing
from tutorial.grpc.geodatas.proto import search_pb2, search_pb2_grpc

logger = logging.getLogger(__name__)

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

port = random.randint(50000, 59000)
stat = statsd.StatsClient('localhost', 8125)

SIGNALS = [signal.SIGINT, signal.SIGTERM]


def _signal_handler(sig, stack):
    """ Empty signal handler used to override python default one """
    pass


class SearchServicer(search_pb2_grpc.SearchServicer):
    @stat.timer("search")
    def search(self, request, context):
        stat.incr("search_count")
        logger.info("search request: " + str(request))
        query = session.query(Thing).filter(
            func.ST_Contains(Thing.geom, 'POINT({} {})'.format(request.lat, request.lng)))
        responses = [search_pb2.SearchResponse(
            response=rec.name) for rec in query]
        logger.info("search responses: " + str(responses))
        return search_pb2.SearchResponses(responses=responses)

    @stat.timer("monitor")
    def monitor(self, request, context):
        stat.incr("monitor_count")
        n_things = session.query(Thing).count()
        return search_pb2.MonitorResponse(n_things=n_things)


def register():
    logger.info("register started")
    c = consul.Consul()
    check = consul.Check.tcp("127.0.0.1", port, "30s")
    c.agent.service.register(
        "search-service",
        "search-service-%d" % port,
        address="127.0.0.1",
        port=port,
        check=check
    )
    logger.info("services: " + str(c.agent.services()))


def unregister():
    logger.info("unregister started")
    c = consul.Consul()
    c.agent.service.deregister("search-service-%d" % port)
    logger.info("services: " + str(c.agent.services()))


# Not working ! :(
def serve(block=True):
    logger.info("Search service, version={}".format(
        pkg_resources.get_distribution('tutorial-grpc-geodatas').version
    ))

    # Register signal handler, only if blocking
    if block:
        for sig in SIGNALS:
            signal.signal(sig, _signal_handler)

    max_number_of_clients = 10
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), maximum_concurrent_rpcs=max_number_of_clients)

    search_pb2_grpc.add_SearchServicer_to_server(SearchServicer(), server)

    grpc_host_and_port = '[::]:' + str(port)
    insecure_port = server.add_insecure_port(grpc_host_and_port)
    if insecure_port == 0:
        logger.error(f"Failed to start gRPC server on {insecure_port}")
        raise ConnectionError

    logger.info(f"Starting server on port {insecure_port}...")
    server.start()
    logger.info("Ready and waiting for connections.")

    if not block:
        return server, insecure_port

        # Wait for a signal before exiting
    sig = signal.sigwait(SIGNALS)
    logger.info('Signal {} received, shutting down...'.format(sig))

    server.stop(5).wait()


def main():
    register()
    serve()
    unregister()


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
    logger.setLevel(logging.DEBUG)

    main()
