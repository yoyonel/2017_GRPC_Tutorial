"""

"""
from tutorial.grpc.geodatas.proto import search_pb2
from tutorial.grpc.geodatas.models import Thing
from tutorial.grpc.geodatas.models import session


def test_search_server(core_rpc_stub):
    test_thing = Thing(
        name="test_thing",
        geom='POLYGON((0 0,1 0,1 1,0 1,0 0))'
    )
    session.add(test_thing)
    session.commit()

    req = search_pb2.SearchRequest(
        query="search_client",
        lat=0.5,
        lng=0.5,
        result_per_page=10
    )
    resp = core_rpc_stub.search(req)
    for response in resp.responses:
        assert response.response == "test_thing"

    req = search_pb2.SearchRequest(
        query="search_client",
        lat=0.0,
        lng=0.0,
        result_per_page=10
    )
    resp = core_rpc_stub.search(req)
    for response in resp.responses:
        assert response.response == ""

    session.delete(test_thing)
    session.commit()
