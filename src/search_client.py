import argparse
import grpc
import sys
import logging
from dns import resolver

import search_pb2


def init_logger(verbose):
    """

    Args:
        verbose (bool):

    Returns:

    """
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG if verbose else logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    log.addHandler(ch)
    return log


def process(args):
    """

    Args:
        args (namedtuple):

    Returns:

    """
    log = init_logger(args.verbose)

    ######################################################################
    consul_resolver = resolver.Resolver()
    consul_resolver.port = args.consul_resolver_port
    consul_resolver.nameservers = args.consul_resolver_nameservers

    dnsanswer = consul_resolver.query("search-service.service.consul", 'A')
    ip = str(dnsanswer[0])
    dnsanswer_srv = consul_resolver.query("search-service.service.consul", 'SRV')
    port = int(str(dnsanswer_srv[0]).split()[2])
    ######################################################################

    ######################################################################
    log.info("creating grpc client based on consul data: ip=%s port=%d" % (ip, port))
    channel = grpc.insecure_channel('%s:%d' % (ip, port))
    stub = search_pb2.SearchStub(channel)
    ######################################################################

    log.debug("args.monitor: {}".format(args.monitor))
    if args.monitor:
        monitresp = stub.monitor(search_pb2.google_dot_protobuf_dot_empty__pb2.Empty())
        log.debug("monitor response: {}".format(monitresp))

    if args.request_position_latlng:
        req = search_pb2.SearchRequest(
            query="search_client",
            lat=args.request_position_latlng[0],
            lng=args.request_position_latlng[1],
            result_per_page=10)
        log.debug("sending request: {}".format(req))
        resp = stub.search(req)
        log.debug("received response: {}".format(resp))


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
    main()
