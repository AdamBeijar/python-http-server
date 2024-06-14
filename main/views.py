from main.responses import HtmlResponse, JsonResponse 

def index(request):
    content = {
        "title": "Python Web Server",
        "content": [
            "This is a simple web server written in Python.",
            "It can serve HTML, CSS, JavaScript, and other files.",
            "It can also serve JSON responses."
        ],
        "names": [
            "Adam Beijar",
            "John Doe"
        ],
        "name": "Adam Beijar"
        }
    return HtmlResponse("template.html", 200, **content)