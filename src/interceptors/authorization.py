import grpc
from grpc_interceptor import ServerInterceptor
from functools import wraps

from jose import jwt
from jose.exceptions import JWTError
from config.authorization import EXCEPT_METHODS

class AuthorizationInterceptor(ServerInterceptor):
    def __init__(self, jwt_secret="a-string-secret-at-least-256-bits-long", jwt_algo='HS256'):
        self.jwt_secret = jwt_secret
        self.jwt_algo = jwt_algo

    def intercept(self, method, request, context, method_name):
        
        # Skip authentication for excepted methods
        if method_name in EXCEPT_METHODS:
            return method(request, context)

        print(method_name)

        metadata = dict(context.invocation_metadata())
        token = metadata.get("authorization")
        decoded_data = None
        is_auth = False

        if not token:
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "Invalid authorization token")

        auth_header = metadata['authorization']
        
        # Check for Bearer token format
        parts = auth_header.split()

        if len(parts) != 2 or parts[0].lower() != 'bearer':
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "Invalid authorization token")

        token = parts[1]

        # Validate JWT
        try:
           decoded_data = jwt.decode(token, self.jwt_secret, algorithms=[self.jwt_algo])
           is_auth = True
        except JWTError:
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "Invalid authorization token")

        # Wrap the original method to include auth information
        @wraps(method)
        def wrapper(request, context):
            if decoded_data:
                # Store auth info in context's user_data dict
                context.is_auth = is_auth
                context.auth_user = decoded_data
            return method(request, context)

        return wrapper(request, context)
