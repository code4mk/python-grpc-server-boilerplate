from google.protobuf.json_format import MessageToDict


def grpc_req_to_dict(grpc_req):
    """
    Convert a gRPC request to a dictionary.
    """
    return MessageToDict(grpc_req, preserving_proto_field_name=True)
