import resources.http_codes 

class Response:
    def __init__(self, status, data):
        self.status = status
        self.data = data
        self.status_text = self.makeStatusText()

    def makeStatusText(self):
        if self.status in resources.http_codes.http_codes:
            return resources.http_codes.http_codes[self.status]
        else:
            return "Unknown Status"

    def __str__(self):
        return f"Response(status={self.status}, data={self.data})"

    def __repr__(self):
        return str(self)
    

    
class JsonResponse(Response):
    def __init__(self, data):
        super().__init__(200, data)
        self.headers = {"Content-Type": "application/json"}

class HtmlResponse(Response):
    def __init__(self, data, status=200):
        super().__init__(status, data)
        self.headers = {"Content-Type": "text/html"}
        self.data = f"HTTP/1.1 {self.status}\nContent-Type: text/html"
        self.data += "\n\n" + data
    