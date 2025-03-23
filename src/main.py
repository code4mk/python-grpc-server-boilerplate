import logging
import signal
from the_grpc.server import GRPCServer
from proto import hello_pb2_grpc
from services.greeter import Greeter

class ServerApp:
    def __init__(self):
        self.server = None

    def add_services(self, server):
        hello_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)

    def start(self):
        logging.basicConfig()
        self.server = GRPCServer(address='0.0.0.0', port=50051)
        self.add_services(self.server.instance)
        self.server.serve()

    def stop(self):
        if self.server:
            self.server.stop()

def main():
    app = ServerApp()
    signal.signal(signal.SIGINT, lambda s, f: app.stop())
    app.start()

if __name__ == '__main__':
    main()
