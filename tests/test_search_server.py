"""
"""
from tutorial.grpc.geodatas.models.thing import Thing
from tutorial.grpc.geodatas.proto import search_pb2


def test_search_server(core_rpc_stub, add_to_session):
    thing_name = "test_squared_thing"
    test_thing = Thing(name=thing_name, geom='POLYGON((0 0,1 0,1 1,0 1,0 0))')
    add_to_session(test_thing)

    def _filter_responses(_responses):
        return list(filter(lambda r: r.response == thing_name, _responses))

    req = search_pb2.SearchRequest(query="search_client", lat=0.5, lng=0.5, result_per_page=10)
    resp = core_rpc_stub.search_thing(req)
    responses = _filter_responses(resp.responses)
    assert len(responses) == 1
    assert responses[0].response == thing_name

    req = search_pb2.SearchRequest(query="search_client", lat=-1.0, lng=0.0, result_per_page=10)
    resp = core_rpc_stub.search_thing(req)
    responses = _filter_responses(resp.responses)
    assert responses == []