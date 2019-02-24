"""
"""
import argparse
import grpc
import logging

from tutorial.grpc.geodatas.proto import search_pb2_grpc, search_pb2
from tutorial.grpc.geodatas.tools.service_discovery import find_service_with_consul

logger = logging.getLogger(__name__)


def get_search_rpc_stub(ip, port):
    """

    :param ip:
    :param port:
    :return:
    """
    logger.info(f"creating grpc client based on consul data: ip={ip} port={port}")
    channel = grpc.insecure_channel(f'{ip}:{port}')
    stub = search_pb2_grpc.SearchStub(channel)
    return stub


def get_search_rpc_stub_with_consul(
        consul_resolver_port,
        consul_resolver_nameservers,
        consul_resolver_nameservice
):
    """

    :param consul_resolver_port:
    :param consul_resolver_nameservers:
    :param consul_resolver_nameservice:
    :return:
    """
    search_service_ip, search_service_port = find_service_with_consul(consul_resolver_port,
                                                                      consul_resolver_nameservers,
                                                                      consul_resolver_nameservice)

    return get_search_rpc_stub(search_service_ip, search_service_port)


def process_monitor(search_service_stub):
    """

    :param search_service_stub:
    :return:
    """
    monitresp = search_service_stub.monitor(search_pb2.google_dot_protobuf_dot_empty__pb2.Empty())
    logger.debug("monitor response: {}".format(monitresp))


def process_request_position(search_service_stub, lat, lng):
    """

    :param search_service_stub:
    :param lat:
    :param lng:
    :return:
    """
    req = search_pb2.SearchRequest(query="search_client",
                                   lat=lat,
                                   lng=lng,
                                   result_per_page=10)
    logger.debug("sending request: {}".format(req))
    resp = search_service_stub.search(req)
    logger.debug("received response: {}".format(resp if resp else 'None'))


def process(args):
    """

    :param args:
    :return:
    """
    search_service_stub = get_search_rpc_stub_with_consul(args.consul_resolver_port,
                                                          args.consul_resolver_nameservers,
                                                          args.consul_resolver_nameservice)

    if args.monitor:
        process_monitor(search_service_stub)

    if args.request_position_latlng:
        process_request_position(search_service_stub, *args.request_position_latlng)


def build_parser(parser=None, **argparse_options):
    """

    Args:
        parser (argparse.ArgumentParser):
        **argparse_options (dict):

    Returns:

    """
    if parser is None:
        parser = argparse.ArgumentParser(**argparse_options)

    parser.add_argument("--request_position_latlng",
                        type=float,
                        nargs=2,
                        required=False,
                        default=None,
                        help="(Lattitude Longitude)")
    #
    parser.add_argument("--consul_resolver.port", dest="consul_resolver_port",
                        type=int,
                        nargs=1,
                        default=8600,
                        help="(default=%(default)s).")
    parser.add_argument("--consul_resolver.nameservers", dest="consul_resolver_nameservers",
                        nargs='+',
                        type=str,
                        default=["127.0.0.1"],
                        help="(default=%(default)s).")
    parser.add_argument("--consul_resolver.nameservice", dest="consul_resolver_nameservice",
                        nargs=1,
                        type=str,
                        default="search-service.service.consul",
                        help="(default=%(default)s).")
    #
    parser.add_argument("-m", "--monitor",
                        action="store_true", default=False,
                        help="")
    # Imports
    parser.add_argument("-v", "--verbose",
                        action="store_true", default=False,
                        help="increase output verbosity")
    # return parsing
    return parser


def parse_arguments():
    """

    Returns:
        argparse.Namespace:
    """
    # return parsing
    return build_parser().parse_args()


def main():
    args = parse_arguments()
    process(args)


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
    logger.setLevel(logging.DEBUG)

    main()
