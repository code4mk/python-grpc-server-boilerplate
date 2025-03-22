from proto import hello_pb2_grpc
from proto import hello_pb2


class Greeter(hello_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        return hello_pb2.HelloResponse(message=f"Hello mr/ms , {request.name}!")