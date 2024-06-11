from main.responses import HtmlResponse

def index(request):
    return HtmlResponse("<h1>Hello, World!</h1> <hr> <p>It's working!</p>", 200)

def login(request):
    return HtmlResponse("<h1>Login</h1>")