import os
import sys
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ServerRestartHandler(FileSystemEventHandler):
    def __init__(self, server_file):
        self.server_file = server_file
        self.process = None
        self.start_server()
    
    def start_server(self):
        # Kill previous process if it exists
        if self.process:
            print("Stopping gRPC server...")
            self.process.terminate()
            self.process.wait()

        
        # Start new server process
        print("Starting gRPC server...")
        self.process = subprocess.Popen([sys.executable, self.server_file])
    
    def on_modified(self, event):
        # Check if it's a Python file
        if event.src_path.endswith('.py'):
            print(f"Detected change in {event.src_path}")
            self.start_server()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python hot_reload.py <server_file.py>")
        sys.exit(1)
    
    server_file = sys.argv[1]
    path = os.path.dirname(os.path.abspath(server_file)) or '.'
    
    event_handler = ServerRestartHandler(server_file)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        if event_handler.process:
            event_handler.process.terminate()
    
    observer.join()