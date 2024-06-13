import socket
import datetime
import traceback
from main import urls
from main.responses import HtmlResponse, JsonResponse, Response
import getopt
import sys
import resources.request as Request
from colorama import Fore, Style, init as colorama_init
import types
from resources.not_found import not_found
import ssl


class Server:
    """A simple HTTP server that listens for incoming connections and handles requests.
    Default port is 8080, can be changed with --port (or -p) flag. Host can be changed with --host (or -h) flag."""
    def __init__(self, port: int = 8080, host: str = "127.0.0.1", cert_file=None, key_file=None):
        # initialize the server socket
        self.port: int = port
        self.host: str = host
        self.cert_file = cert_file
        self.key_file = key_file
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((host, self.port))
        colorama_init()

    def start(self):
        """Start the server and listen for incoming connections."""
        self.server_socket.listen()
        self.welcome_message()
        try:
            while True:
                try:
                    client_socket, addr = self.server_socket.accept()
                    if self.cert_file and self.key_file:
                        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
                        context.load_cert_chain(certfile=self.cert_file, keyfile=self.key_file)
                        client_socket = context.wrap_socket(client_socket, server_side=True)
                    request = client_socket.recv(1024)
                    request = self.handle_request(request)
                    if not request:
                        continue
                    response = self.handle_response(request, addr)
                    client_socket.send(response.encode())
                    client_socket.close()
                except Exception as e:
                    print(f"An error occurred: {e}")
                    traceback.print_exc()
        except KeyboardInterrupt:
            self.stop()
        except Exception as e:
            print("An error occurred: ")
            traceback.print_exc()

    def stop(self):
        self.server_socket.close()

    def welcome_message(self):
        # Sends the welcome message when you start the server
        # clear the console
        print("\033[H\033[J")
        print(datetime.datetime.now().strftime("%A, %B %d, %Y %H:%M:%S"))
        uri = self.host + ":" + str(self.port)
        print(f"Server is running on {self.link(uri, 'http://' + uri)}")
        print("--host and --port flags can be used to change the host and port")
        print("Press CTRL + C to stop the server")

    def link(self, uri, label=None):
        if label is None:
            label = uri
        parameters = ''

        # OSC 8 ; params ; URI ST <name> OSC 8 ;; ST
        escape_mask = '\033]8;{};{}\033\\{}\033]8;;\033\\'
        return escape_mask.format(parameters, uri, label)

    def handle_request(self, request):
        """Parse the incoming request and return a Request object."""
        try:
            request = request.decode()
        except UnicodeDecodeError:
            print("Error decoding request, cannot handle https requests yet.")
            return
        parsed_request = Request.Request(request)
        return parsed_request

    def handle_path(self, path: str, request) -> Response:
        url = self.path_in_urls(path, request.method)
        return url(request) # type: ignore

    def path_in_urls(self, path: str, method: str):
        found = False
        foundUrl = None
        notFoundFound = False
        notFoundURL = None
        for url in urls.urls:
            path, url_path = self.fix_paths(path, url.path)
            if path.startswith(url_path) and (isinstance(url.name, types.ModuleType) or url.include):
                if isinstance(url.name, types.ModuleType):
                    return self.handle_include(url.name.urls, path.replace(url_path, "", 1), method)
                elif url.include:
                    return self.handle_include(url.include, path.replace(url_path, "", 1), method)
            if path == url_path and url.method == method:
                found = True
                foundUrl = url
                break
            elif "*" in url_path and url.method == method:
                notFoundFound = True
                notFoundURL = url
        if found:
            return foundUrl
        elif notFoundFound:
            return notFoundURL
        return not_found()

    def handle_include(self, url, path, method):
        found = False
        foundUrl = None
        notFoundFound = False
        notFoundURL = None
        for url in url:
            path, url_path = self.fix_paths(path, url.path)
            if path.startswith(url_path) and (isinstance(url.name, types.ModuleType) or url.include):
                if isinstance(url.name, types.ModuleType):
                    return self.handle_include(url.name.urls, path.replace(url_path, "", 1), method)
                elif url.include:
                    return self.handle_include(url.include, path.replace(url_path, "", 1), method)
            if path == url_path and url.method == method:
                found = True
                foundUrl = url
                break
            elif "*" in url_path and url.method == method:
                notFoundFound = True
                notFoundURL = url
        if found:
            return foundUrl
        elif notFoundFound:
            return notFoundURL
        return not_found()

    def fix_paths(self, path: str, url: str):
        if path.startswith("/"):
            path = path[1:]
        if path.endswith("/"):
            path = path[:-1]
        if url.startswith("/"):
            url = url[1:]
        if url.endswith("/"):
            url = url[:-1]
        return path.lower(), url.lower()

    def build_response(self, status: str, status_text: str, data, addr, request) -> str:
        current_time = datetime.datetime.now().strftime("%d/%b/%Y %H:%M:%S")
        return_response = ""
        error_response = False
        if int(status) >= 400:
            return_response += f"{request.method } {request.path} {status} {status_text}\n"
            error_response = True
        if error_response:
            return_response += f'[{current_time}] \033[1m{Fore.RED}\"{request.method} {request.path}\"{Style.RESET_ALL} {status}'
        else:
            return_response += f'[{current_time}] {Fore.GREEN}\"{request.method} {request.path}\"{Style.RESET_ALL} {status}'
        return return_response

    def handle_response(self, request, addr) -> str: # type: ignore
        response = self.handle_path(request.path, request) # type: ignore
        print(self.build_response(response.status, response.status_text, response.data, addr, request))
        return response.data


if __name__ == "__main__":
    port = 8080
    host = "127.0.0.1"
    cert = None
    key = None
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:p:", ["host=", "port=", "cert=", "key="])
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--host"):
            host = arg
        elif opt in ("-p", "--port"):
            port = int(arg)
        elif opt == "--cert":
            cert = arg
        elif opt == "--key":
            key = arg
    server = Server(port=port, host=host, cert_file=cert, key_file=key)
    server.start()
