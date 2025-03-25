from proto import hello_pb2_grpc
from proto import hello_pb2


class Greeter(hello_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        # Get both auth status and user data
        is_authenticated = getattr(context, 'is_auth', False)
        auth_user_data = getattr(context, 'auth_user', {})
        
        print(f"Is authenticated: {is_authenticated}")
        print(f"User data: {auth_user_data}")
        
        # Handle case where name is None or empty
        name = request.name if request.name else "Guest"
        return hello_pb2.HelloResponse(message=f"Hello mr/ms, {name}!")
