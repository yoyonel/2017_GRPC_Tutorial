"""

"""
from concurrent import futures
import grpc
import logging
import pkg_resources
import random
import signal

from tutorial.grpc.geodatas.proto import search_pb2_grpc
from tutorial.grpc.geodatas.rpc.search_servicer import SearchServicer
from tutorial.grpc.geodatas.tools.service_discovery import consuled

logger = logging.getLogger(__name__)

SIGNALS = [signal.SIGINT, signal.SIGTERM]


def _signal_handler(_sig, _stack):
    """ Empty signal handler used to override python default one """
    pass


def serve(block=True, port: int = random.randint(50000, 59000)):
    """

    :param block:
    :param port:
    :return:
    """
    logger.info("Search service, version={}".format(pkg_resources.get_distribution('tutorial-grpc-geodatas').version))

    # Register signal handler, only if blocking
    if block:
        for sig in SIGNALS:
            signal.signal(sig, _signal_handler)

    max_number_of_clients = 10
    # Creates Server with which RPCs can be serviced
    # https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.Executor
    # https://stackoverflow.com/questions/51089746/grpc-python-thread-pool-vs-max-concurrent-rpcs
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10),
                         maximum_concurrent_rpcs=max_number_of_clients)
    # Register Rpc Handlers with `SearchServicer` server
    search_pb2_grpc.add_SearchServicer_to_server(SearchServicer(), server)

    # Opens an insecure port for accepting RPCs.
    grpc_host_and_port = f'[::]:{port}'
    insecure_port = server.add_insecure_port(grpc_host_and_port)
    if insecure_port == 0:
        logger.error(f"Failed to start gRPC server on {insecure_port}")
        raise ConnectionError

    with consuled(insecure_port):
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
    serve()


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
    logger.setLevel(logging.DEBUG)

    main()
