import grpc
from jose import jwt
from jose.exceptions import JWTError

class AuthorizationInterceptor(grpc.ServerInterceptor):
    def __init__(self, jwt_secret="a-string-secret-at-least-256-bits-long", jwt_algo='HS256'):
        self.jwt_secret = jwt_secret
        self.jwt_algo = jwt_algo
        
        def abort(ignored_request, context):
            context.abort(grpc.StatusCode.UNAUTHENTICATED, 'Invalid or missing authorization token')

        self._abort = grpc.unary_unary_rpc_method_handler(abort)

    def intercept_service(self, continuation, handler_call_details):
        metadata = dict(handler_call_details.invocation_metadata)
        print(metadata.get('authorization'))

        if 'authorization' not in metadata:
            return self._abort
            
        auth_header = metadata['authorization']
        
        # Check for Bearer token format
        parts = auth_header.split()

        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return self._abort
            
        token = parts[1]

        # Validate JWT
        try:
            jwt.decode(token, self.jwt_secret, algorithms=[self.jwt_algo])

        except JWTError:
            return self._abort
            
        return continuation(handler_call_details) 