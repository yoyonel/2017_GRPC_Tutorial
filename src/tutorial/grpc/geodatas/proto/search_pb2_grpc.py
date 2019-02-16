# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from tutorial.grpc.geodatas.proto import search_pb2 as tutorial_dot_grpc_dot_geodatas_dot_proto_dot_search__pb2


class SearchStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.monitor = channel.unary_unary(
        '/Search/monitor',
        request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
        response_deserializer=tutorial_dot_grpc_dot_geodatas_dot_proto_dot_search__pb2.MonitorResponse.FromString,
        )
    self.search = channel.unary_unary(
        '/Search/search',
        request_serializer=tutorial_dot_grpc_dot_geodatas_dot_proto_dot_search__pb2.SearchRequest.SerializeToString,
        response_deserializer=tutorial_dot_grpc_dot_geodatas_dot_proto_dot_search__pb2.SearchResponses.FromString,
        )


class SearchServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def monitor(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def search(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_SearchServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'monitor': grpc.unary_unary_rpc_method_handler(
          servicer.monitor,
          request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
          response_serializer=tutorial_dot_grpc_dot_geodatas_dot_proto_dot_search__pb2.MonitorResponse.SerializeToString,
      ),
      'search': grpc.unary_unary_rpc_method_handler(
          servicer.search,
          request_deserializer=tutorial_dot_grpc_dot_geodatas_dot_proto_dot_search__pb2.SearchRequest.FromString,
          response_serializer=tutorial_dot_grpc_dot_geodatas_dot_proto_dot_search__pb2.SearchResponses.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'Search', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
