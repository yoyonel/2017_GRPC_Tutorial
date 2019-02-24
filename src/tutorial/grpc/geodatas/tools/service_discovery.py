"""
"""
import consul
from decorator import contextmanager
from dns import resolver as dns_resolver
from dns import exception as dns_exception
import logging
import os
from typing import List, Tuple

logger = logging.getLogger(__name__)


def generate_service_id(service_name: str, port: int) -> str:
    """

    :param service_name:
    :param port:
    :return:
    """
    return f"{service_name}-{port}"


def register_to_consul(port: int, service_name: str = "search-service"):
    """
    TODO: need to handle exceptions

    :param port:
    :param service_name:
    :return:
    """
    logger.info("register started")
    consul_host = os.environ.get("TUTORIAL_GRPC_CONSUL_HOST", "127.0.0.1")
    logging.debug(f"consul_host={consul_host}")
    c = consul.Consul(host=consul_host)
    check = consul.Check.tcp(consul_host, port, "30s")

    c.agent.service.register(
        name=service_name,
        service_id=generate_service_id(service_name, port),
        address=consul_host,
        port=port,
        check=check
    )
    logger.info("services: " + str(c.agent.services()))


def unregister_to_consul(port: int, service_name: str = "search-service"):
    """

    :param port:
    :param service_name:
    :return:
    """
    logger.info("unregister started")
    c = consul.Consul()
    c.agent.service.deregister(service_id=generate_service_id(service_name, port))
    logger.info("services: " + str(c.agent.services()))


def find_service_with_consul(consul_resolver_port: int,
                             consul_resolver_nameservers: List[str],
                             consul_service_name: str = "search-service.service.consul") -> Tuple[str, int]:
    """

    :param consul_resolver_port:
    :param consul_resolver_nameservers:
    :param consul_service_name:
    :return:
    """
    consul_resolver = dns_resolver.Resolver()
    consul_resolver.port = consul_resolver_port
    consul_resolver.nameservers = consul_resolver_nameservers

    # TODO: Need to refactor the extraction of service name from consul service name
    try:
        service_name = consul_service_name.split('.')[0]
    except IndexError:
        service_name = consul_service_name

    try:
        dnsanswer = consul_resolver.query(consul_service_name, 'A', lifetime=5)
    except dns_exception.Timeout:
        raise ConnectionError(f"[dns.exception.Timeout] Can't reach consul resolver at port={consul_resolver_port} !")
    except dns_resolver.NoNameservers:
        raise ConnectionError(f"Can't find consul service={consul_service_name} => "
                              f"`{service_name}` server not started/synced/checked !")
    service_ip = str(dnsanswer[0])
    dnsanswer_srv = consul_resolver.query("search-service.service.consul", 'SRV')
    service_port = int(str(dnsanswer_srv[0]).split()[2])

    return service_ip, service_port


@contextmanager
def consuled(port: int, service_name: str = "search-service"):
    """Context manager for register/unregister search service.

    "PEP 343 -- The "with" Statement": https://www.python.org/dev/peps/pep-0343/

    :param port:
    :param service_name:
    :return:
    """
    register_to_consul(port, service_name)
    try:
        yield
    finally:
        unregister_to_consul(port, service_name)
