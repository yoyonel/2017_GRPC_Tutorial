"""

"""
import argparse
import grpc
import logging
import dns
from dns import resolver

from tutorial.grpc.geodatas.proto import search_pb2_grpc, search_pb2

logger = logging.getLogger(__name__)


def find_search_service_with_consul(consul_resolver_port, consul_resolver_nameservers):
    """

    :param consul_resolver_port:
    :param consul_resolver_nameservers:
    :return:
    """
    consul_resolver = resolver.Resolver()
    consul_resolver.port = consul_resolver_port
    consul_resolver.nameservers = consul_resolver_nameservers

    consul_service_name = "search-service.service.consul"
    try:
        dnsanswer = consul_resolver.query(consul_service_name, 'A', lifetime=5)
    except dns.exception.Timeout:
        raise RuntimeError(
            f"[dns.exception.Timeout] Can't reach consul resolver at port={consul_resolver_port} !")
    except dns.resolver.NoNameservers:
        raise RuntimeError(f"Can't find consul service={consul_service_name} => "
                           f"`Search-service` server not started/synced/checked !")
    ip = str(dnsanswer[0])
    dnsanswer_srv = consul_resolver.query("search-service.service.consul", 'SRV')
    port = int(str(dnsanswer_srv[0]).split()[2])

    return ip, port


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


def process(args):
    """

    Args:
        args (namedtuple):

    Returns:

    """
    ip, port = find_search_service_with_consul(args.consul_resolver_port, args.consul_resolver_nameservers)

    stub = get_search_rpc_stub(ip, port)

    logger.debug("args.monitor: {}".format(args.monitor))
    if args.monitor:
        monitresp = stub.monitor(search_pb2.google_dot_protobuf_dot_empty__pb2.Empty())
        logger.debug("monitor response: {}".format(monitresp))

    if args.request_position_latlng:
        req = search_pb2.SearchRequest(
            query="search_client",
            lat=args.request_position_latlng[0],
            lng=args.request_position_latlng[1],
            result_per_page=10)
        logger.debug("sending request: {}".format(req))
        resp = stub.search(req)
        logger.debug("received response: {}".format(resp))


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
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
    logger.setLevel(logging.DEBUG)

    main()
