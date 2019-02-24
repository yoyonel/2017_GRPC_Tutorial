"""
"""
from grpc import insecure_channel
import logging
from typing import List

from tutorial.grpc.geodatas.proto import search_pb2_grpc
from tutorial.grpc.geodatas.tools.service_discovery import find_service_with_consul

logger = logging.getLogger(__name__)


def get_search_rpc_stub(ip: str, port: int) -> search_pb2_grpc.SearchStub:
    """

    :param ip:
    :param port:
    :return:
    """
    logger.info(f"creating grpc client based on consul data: ip={ip} port={port}")
    channel = insecure_channel(f'{ip}:{port}')
    stub = search_pb2_grpc.SearchStub(channel)
    return stub


def get_search_rpc_stub_with_consul(consul_resolver_port: int,
                                    consul_resolver_nameservers: List[str],
                                    consul_resolver_nameservice: str) -> search_pb2_grpc.SearchStub:
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
