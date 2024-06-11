class Request:
    def __init__(self, request):
        request = self.parse_http_request(request)
        self.method = request["method"]
        self.path = request["path"]
        self.protocol = request["protocol"]
        self.headers = request["headers"]
        self.content_type = self.headers.get("Content-Type")
        if request.get("form"):
            self.form = request["form"]
        else:
            self.form = None

    def parse_http_request(self, request):
            lines = request.split("\n")
            request_line = lines[0]
            headers = {}
            for line in lines[1:]:
                if ":" in line and line != "\r\n":
                    split_line = line.split(":")
                    key = split_line[0]
                    value = split_line[1]
                    headers[key] = value.strip()
                    if key == "Content-Type" and "boundary" in value:
                        headers["boundary"] = value.split("=")[1]
                        headers["Content-Type"] = "multipart/form-data"
            content: dict = self.handle_content_types(headers, request)
            method, path, protocol = request_line.split(" ")
            if headers.get("Content-Type") == "multipart/form-data":
                return_dict = {
                    "method": method,
                    "path": path,
                    "protocol": protocol,
                    "headers": headers,
                    "form": content
                }
                return return_dict
            return {
                "method": method,
                "path": path,
                "protocol": protocol,
                "headers": headers,
            }
    
    def handle_content_types(self, headers, request) -> dict:
        content_type = headers.get("Content-Type")
        if content_type == "application/json":
            pass
        elif content_type == "application/x-www-form-urlencoded":
            pass
        elif content_type == "multipart/form-data":
            return self.handle_multipart_form_data(headers, request)
        return {}

    def handle_json(self, request):
        pass

    def handle_form_urlencoded(self, request):
        pass

    def handle_multipart_form_data(self, headers, request) -> dict:
        form = request.split(headers["boundary"])
        form_dict = {}
        for key in form[2:]:
            current_key = key.split(";")[1].split("=")[1].strip().split("\r\n")[0].replace('"', "")
            value = key.split(";")[1].split("=")[1].strip().split("\r\n")[2]
            form_dict[current_key] = value
        return form_dict

    def GET(self, key):
        if self.form:
            return self.form.get(key)
        else:
            raise Exception("No form data")

    def __str__(self):
        returnstr = f"""
        Method: {self.method}
        Path: {self.path}
        Protocol: {self.protocol}
        Headers: {self.headers}
        """
        if self.form:
            returnstr += f"Form: {self.form}"
        return returnstr