import grpc
from grpc_interceptor import ServerInterceptor
from loguru import logger

# Configure Loguru
logger.add("grpc_server.log", rotation="10MB", level="INFO")

class LoggingInterceptor(ServerInterceptor):
    def intercept(self, method, request, context, method_name):
        
        response = method(request, context)
        logger.info(
            "gRPC Request | "
            f"Method: {method_name} | "
            f"Request: {request}"
        )
        logger.info(
            "gRPC Response | "
            f"Method: {method_name} | "
            f"Response: {response}"
        )
        return response