import grpc
from grpc_interceptor import ServerInterceptor
from loguru import logger

# Configure Loguru
logger.add("grpc_server.log", rotation="10MB", level="INFO")


class LoggingInterceptor(ServerInterceptor):
    def intercept(self, method, request, context, method_name):
        try:
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
        except Exception as e:
            # Log the error
            logger.error(
                f"Error in gRPC call | "
                f"Method: {method_name} | "
                f"Request: {request} | "
                f"Error: {str(e)}"
            )
 
            # Re-raise the exception to maintain the original behavior
            raise