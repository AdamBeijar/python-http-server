class path:
    def __init__(self, path, name, view, method):
        self.path = path
        self.name = name
        self.view = view
        self.method = method
        self.args = []

    def __call__(self, request):
        return self.view(request)

    def __str__(self):
        return self.path
    
    def __contains__(self, item):
        return item in self.path
