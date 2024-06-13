from main.responses import HtmlResponse, JsonResponse
from resources.request import Request


def index(request: Request):
    kwargs = {
        "title": request.params.get("title"),
        "content": "<p>Hello, World!</p>",
        "footer": "<p>Footer</p>"
        }
    return HtmlResponse("template.html", 200, **kwargs)


def getUsers(request: Request):
    users = [
        {"name": "John", "age": 25},
        {"name": "Jane", "age": 22},
        {"name": "Bob", "age": 30},
    ]
    return JsonResponse(users, 200)

def notFound(request: Request):
    return HtmlResponse("404.html", 404)