import socket
import datetime
import traceback
from main import urls
from main.responses import HtmlResponse
import getopt
import sys
import resources.request as Request

class Server:
    def __init__(self, port: int=8080, host: str="127.0.0.1"):
        self.port: int = port
        self.host: str = host
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((host, self.port))

    def start(self):
        self.server_socket.listen()
        self.welcome_message()
        try:
            while True:
                client_socket, addr = self.server_socket.accept()
                request = client_socket.recv(1024) # type: ignore
                request: Request = self.handle_request(request)
                response = self.handle_response(request, addr)
                client_socket.send(response.encode())
                client_socket.close()
        except KeyboardInterrupt:
            self.stop()
        except Exception as e:
            print("An error occurred: ")
            traceback.print_exc()
            self.stop()

    def stop(self):
        self.server_socket.close()

    def welcome_message(self):
        # clear the console
        print("\033[H\033[J")
        print(datetime.datetime.now().strftime("%A, %B %d, %Y %H:%M:%S"))
        print(f"Server is running on {self.host}:{self.port}")
        print("--host and --port flags can be used to change the host and port")
        print("Press CTRL + C to stop the server")

    def handle_request(self, request) -> Request:
        request = request.decode()
        parsed_request = Request.Request(request)
        return parsed_request
    
    def handle_path(self, path: str, request: Request) -> str:
        url = self.path_in_urls(path)
        if url:
            return url(request) # type: ignore
        return HtmlResponse("<h1>404 Not Found</h1>", 404) # type: ignore
    
    def path_in_urls(self, path: str) -> bool:
        for url in urls.urls:
            if path == url.path:
                return url # type: ignore
        return False
    
    def build_response(self, status: str, status_text: str, data, addr, request) -> str:
        current_time = datetime.datetime.now().strftime("%d/%b/%Y %H:%M:%S")
        return_response = ""
        if int(status) >= 400:
            return_response += f"{request.method } {request.path} {status} {status_text}\n"
        return_response += f'[{current_time}] \"{request.method} {request.path}\" {status}'
        return return_response 
    
    def handle_response(self, request: Request, addr) -> str: # type: ignore
        response = self.handle_path(request.path, request) # type: ignore
        if type(response) == HtmlResponse:
            print(self.build_response(response.status, response.status_text, response.data, addr, request))
            return response.data


if __name__ == "__main__":
    port = 8080
    host = "127.0.0.1"    
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:p:", ["host=", "port="])
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--host"):
            host = arg
        elif opt in ("-p", "--port"):
            port = int(arg)
    server = Server(port=port, host=host)
    server.start()