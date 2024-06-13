from resources.path import path
from main.responses import HtmlResponse

def not_found():
    return path("/not_found", "not_found", not_found_view, "GET")

def not_found_view(request):
    return HtmlResponse("<head><title>404 Not Found</title></head><body><h1>404 Not Found</h1></body>", 404)