import logging
import signal
from the_grpc.server import GRPCServer
from proto import hello_pb2_grpc
from services.greeter import Greeter
from interceptors.authorization import AuthorizationInterceptor
from interceptors.logging import LoggingInterceptor

class ServerApp:
    def __init__(self, interceptors=[]):
        self.server = None
        self.interceptors = interceptors

    def add_services(self, server):
        hello_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
        # add other services here

    def start(self):
        logging.basicConfig()
        self.server = GRPCServer(address='127.0.0.1', port=50051, interceptors=self.interceptors)
        self.add_services(self.server.instance)
        self.server.serve()

    def stop(self):
        if self.server:
            self.server.stop()

def main():
    interceptors = [AuthorizationInterceptor(), LoggingInterceptor()]
    app = ServerApp(interceptors=interceptors)
    signal.signal(signal.SIGINT, lambda s, f: app.stop())
    app.start()

if __name__ == '__main__':
    main()
