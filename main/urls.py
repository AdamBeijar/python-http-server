from frontend import views
from resources.path import path

urls = {
    path("/", "index", views.index, "GET"),
    path("/login", "login", views.login, "GET"),
}