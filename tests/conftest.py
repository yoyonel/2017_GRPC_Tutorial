import grpc
import pytest

from tutorial.grpc.geodatas.proto import search_pb2_grpc
from tutorial.grpc.geodatas.search_server import serve


@pytest.fixture(scope="session", autouse=True)
def start_core_rpc_server(request):
    """
    Spawn an instance of the rpc service, and close it at the end of test sessions
    :param request:
    :type request:
    :return:
    :rtype:
    """
    server, insecure_port = serve(block=False)
    assert server is not None
    pytest.insecure_port = insecure_port

    def _kill_server():
        server.stop(0)

    request.addfinalizer(_kill_server)


@pytest.fixture
def core_rpc_stub(request):
    """
    Create a new rpc stub and connect to the server

    :param request:
    :type request:
    :return:
    :rtype:
    """

    # FIXME: add a way to configure host and port

    channel = grpc.insecure_channel(f'localhost:{pytest.insecure_port}')
    stub = search_pb2_grpc.SearchStub(channel)

    return stub
