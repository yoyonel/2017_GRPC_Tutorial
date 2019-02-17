"""
"""
import consul
import logging

logger = logging.getLogger(__name__)


def register_to_consul(port):
    """
    TODO: need to handle exceptions
    """
    logger.info("register started")
    c = consul.Consul()
    check = consul.Check.tcp("127.0.0.1", port, "30s")
    c.agent.service.register(
        "search-service",
        f"search-service-{port}",
        address="127.0.0.1",
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
