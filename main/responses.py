import resources.http_codes 
import traceback
import json

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
    def __init__(self, data, status=200):
        super().__init__(status, data)
        self.headers = {"Content-Type": "application/json"}
        self.data = f"HTTP/1.1 {self.status}\nContent-Type: application/json \n\n"
        self.data += json.dumps(data)

class HtmlResponse(Response):
    def __init__(self, data, status=200, *args, **kwargs):
        super().__init__(status, data)
        self.headers = {"Content-Type": "text/html"}
        self.data = f"HTTP/1.1 {self.status}\nContent-Type: text/html"
        self.calledFrom = "/".join(traceback.extract_stack()[-2].filename.split("/")[:-1:]) + "/templates/"
        if (htmlFile := self.isTemplate(data)):
            with open(htmlFile, "r") as f:
                htmlData = f.read()
            if kwargs:
                htmlData = self.buildHtml(htmlData, **kwargs)
            self.data += "\n\n" + htmlData 
        else:
            self.data += "\n\n" + data

    def isTemplate(self, data):
        if data.endswith(".html"):
            return self.calledFrom + data
    
    def buildHtml(self, html, **kwargs):
        for key, value in kwargs.items():
            html = html.replace(f"%% {key} %%", str(value))
        return html