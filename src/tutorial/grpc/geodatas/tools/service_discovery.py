"""
"""
import consul
import logging
import os

logger = logging.getLogger(__name__)


def register_to_consul(port):
    """
    TODO: need to handle exceptions
    """
    logger.info("register started")
    consul_host = os.environ.get("TUTORIAL_GRPC_CONSUL_HOST", "127.0.0.1")
    logging.debug(f"consul_host={consul_host}")
    c = consul.Consul(host=consul_host)
    check = consul.Check.tcp(consul_host, port, "30s")
    c.agent.service.register(
        "search-service",
        f"search-service-{port}",
        address=consul_host,
        port=port,
        check=check
    )
    logger.info("services: " + str(c.agent.services()))


def unregister_to_consul(port):
    """
    """
    logger.info("unregister started")
    c = consul.Consul()
    c.agent.service.deregister(f"search-service-{port}")
    logger.info("services: " + str(c.agent.services()))
