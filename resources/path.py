import traceback
import types

class path:
    def __init__(self, path, name=None, view=None, method=None, include=None):
        self.path = path
        self.name = name
        self.view = view
        self.method = method
        self.args = []
        self.include = include

    def __call__(self, request):
        if self.view:
            return self.view(request)
        else:
            return "No view found"

    def __str__(self):
        return self.path
    