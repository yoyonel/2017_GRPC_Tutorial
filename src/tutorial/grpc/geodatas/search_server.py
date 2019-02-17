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
import time

from tutorial.grpc.geodatas.models import session, Thing
from tutorial.grpc.geodatas.proto import search_pb2, search_pb2_grpc

log = logging.getLogger()
log.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)

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
        log.info("search request: " + str(request))
        query = session.query(Thing).filter(
            func.ST_Contains(Thing.geom, 'POINT({} {})'.format(request.lat, request.lng)))
        responses = [search_pb2.SearchResponse(
            response=rec.name) for rec in query]
        log.info("search responses: " + str(responses))
        return search_pb2.SearchResponses(responses=responses)

    @stat.timer("monitor")
    def monitor(self, request, context):
        stat.incr("monitor_count")
        n_things = session.query(Thing).count()
        return search_pb2.MonitorResponse(n_things=n_things)


def register():
    log.info("register started")
    c = consul.Consul()
    check = consul.Check.tcp("127.0.0.1", port, "30s")
    c.agent.service.register(
        "search-service",
        "search-service-%d" % port,
        address="127.0.0.1",
        port=port,
        check=check
    )
    log.info("services: " + str(c.agent.services()))


def unregister():
    log.info("unregister started")
    c = consul.Consul()
    c.agent.service.deregister("search-service-%d" % port)
    log.info("services: " + str(c.agent.services()))


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    search_pb2_grpc.add_SearchServicer_to_server(
        SearchServicer(), server)
    server.add_insecure_port('[::]:' + str(port))
    server.start()
    log.info("server started")
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


# Not working ! :(
def serve_2(block=True):
    """
    Start a new instance of the core service.

    If the server can't be started, a ConnectionError exception is raised

    :param block: If True, block until interrupted. If False, start the server and return directly
    :type block: bool

    :return: If ``block`` is True, return nothing. If ``block`` is False, return the server instance
    :rtype: None | grpc.server
    """
    global port
    # FIXME: We need a configuration file at some points

    log.info("Search-Server, version: {}".format(
        pkg_resources.get_distribution('tutorial-grpc-geodatas').version
    ))

    # Register signal handler, only if blocking
    if block:
        for sig in SIGNALS:
            signal.signal(sig, _signal_handler)

    # We set this number high to allow basically anyone to connect with us
    max_number_of_clients = 500
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=max_number_of_clients),
        maximum_concurrent_rpcs=max_number_of_clients
    )

    grpc_host_and_port = f"[::]:{port}"
    port = server.add_insecure_port(grpc_host_and_port)
    if port == 0:
        log.error("Failed to start gRPC server on {}".format(grpc_host_and_port))
        raise ConnectionError

    log.info(f"Starting server on port {port}...")
    server.start()
    log.info("Ready and waiting for connections.")

    if not block:
        return server

    # Wait for a signal before exiting
    sig = signal.sigwait(SIGNALS)
    log.info('Signal {} received, shutting down...'.format(sig))

    server.stop(5).wait()


def main():
    register()
    serve()
    unregister()


if __name__ == '__main__':
    main()
