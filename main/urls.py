from frontend import views
from resources.path import path
from resources.include import include

urls = [
    path("/api", include("api/urls.py")),
    path("/", include("frontend/urls.py")),
]