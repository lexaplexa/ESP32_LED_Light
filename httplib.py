request_methods = ["GET","HEAD","POST","PUT","DELETE","CONNECT","OPTIONS","TRACE","PATCH"]
response_codes = {
        # 1×× Informational
        100:"Continue",
        101:"Switching Protocols",
        102:"Processing",
        # 2×× Success
        200:"OK",
        201:"Created",
        202:"Accepted",
        203:"Non-authoritative Information",
        204:"No Content",
        205:"Reset Content",
        206:"Partial Content",
        207:"Multi-Status",
        208:"Already Reported",
        226:"IM Used",
        # 3×× Redirection
        300:"Multiple Choices",
        301:"Moved Permanently",
        302:"Found",
        303:"See Other",
        304:"Not Modified",
        305:"Use Proxy",
        307:"Temporary Redirect",
        308:"Permanent Redirect",
        # 4×× Client Error
        400:"Bad Request",
        401:"Unauthorized",
        402:"Payment Required",
        403:"Forbidden",
        404:"Not Found",
        405:"Method Not Allowed",
        406:"Not Acceptable",
        407:"Proxy Authentication Required",
        408:"Request Timeout",
        409:"Conflict",
        410:"Gone",
        411:"Length Required",
        412:"Precondition Failed",
        413:"Payload Too Large",
        414:"Request-URI Too Long",
        415:"Unsupported Media Type",
        416:"Requested Range Not Satisfiable",
        417:"Expectation Failed",
        418:"I'm a teapot",
        421:"Misdirected Request",
        422:"Unprocessable Entity",
        423:"Locked",
        424:"Failed Dependency",
        426:"Upgrade Required",
        428:"Precondition Required",
        429:"Too Many Requests",
        431:"Request Header Fields Too Large",
        444:"Connection Closed Without Response",
        451:"Unavailable For Legal Reasons",
        499:"Client Closed Request",
        # 5×× Server Error
        500:"Internal Server Error",
        501:"Not Implemented",
        502:"Bad Gateway",
        503:"Service Unavailable",
        504:"Gateway Timeout",
        505:"HTTP Version Not Supported",
        506:"Variant Also Negotiates",
        507:"Insufficient Storage",
        508:"Loop Detected",
        510:"Not Extended",
        511:"Network Authentication Required",
        599:"Network Connect Timeout Error"}

class Http:
    def __init__(self):
        self._port = 80
        self._route_functions = {}
        self.request = Request()
        self.response = Response()

    def run(self, port = 80):
        self._port = port
        import usocket
        import sys

        # Create http server
        server = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
        try:
            server.bind(('', port))
        except:
            print('# Bind failed. ')
            sys.exit()
        server.listen(5)

        while True:
            client, addr = server.accept()
            print("["+str(addr[0])+":"+str(addr[1])+"]: Connected")

            # When no data received, raise exception
            client.settimeout(0.2)
            try:
                data = client.recv(1024)
            except:
                client.close()
                print("["+str(addr[0])+":"+str(addr[1])+"]: No request. Disconnected")
                continue
            
            # Parse received data
            self.request.parse(data)
            print("["+str(addr[0])+":"+str(addr[1])+"]: Method:  " + self.request.method)
            print("["+str(addr[0])+":"+str(addr[1])+"]: Url:     " + self.request.url)
            print("["+str(addr[0])+":"+str(addr[1])+"]: Header:  " + str(self.request.headers))
            print("["+str(addr[0])+":"+str(addr[1])+"]: Content: " + str(self.request.content))

            # Call routed funtion
            try:
                self.response.body = self._route_functions[self.request.url]()
            except KeyError:
                client.sendall("Unknown URL")
                client.close()
                print("["+str(addr[0])+":"+str(addr[1])+"]: Unknown url. Disconnected")
                continue

            # Send response
            client.sendall(self.response.create())

            client.close()
            print("["+str(addr[0])+":"+str(addr[1])+"]: Disconnected")

    def route(self, url):
        def wrap(f):
            self._route_functions[url] = f
            return f
        return wrap

class Request():
    def __init__(self):
        self.method = ""
        self.url = ""
        self.version = ""
        self.headers = {}
        self.content = ""

    def parse(self, data):
        # Set to default
        self.method = ""
        self.url = ""
        self.version = ""
        self.headers = {}
        self.content = ""

        # Convert UTF-8 characters to bytes
        data = self._convert_request_utf8(data)

        # Separate http header from body
        data = data.decode('utf-8').split("\r\n\r\n")

        # Split head to rows
        rows = data[0].split("\r\n")

        try:
            # First row is different from other rows
            self.method, self.url, self.version = rows[0].split()
        except:
            return

        # Create a dictionary from remaining rows
        for header in rows[1:]: 
            header = header.split(":")
            self.headers.update({header[0].strip():header[1].strip()})

        # Check methods which sending content
        if self.method == "POST":
            content_type = self.get_header("Content-Type")

            if content_type in ["application/x-www-form-urlencoded"]:
                content = data[1].split("&")
                temp = []
                for element in content: 
                    temp.extend(element.split("="))
                    self.content = {temp[i]:temp[i+1] for i in range(0,len(temp),2)}

            elif content_type in ["application/json", "text/json"]:
                import ujson
                self.content = ujson.load(data[1])

            else:
                self.content = data[1]

        return

    def get_header(self, key):
        try:
            return self.headers[key]
        except KeyError:
            return None

    def _convert_request_utf8(self, data):
        # Convert UTF-8 characters to bytes
        # Example: "%C3%BD" >> b'\xc3\xbd'
        while(1):
            pos = data.find(b'%')
            if pos == -1:
                return data
            data = data[:pos]+bytes([int(data[pos+1:pos+3],16)])+data[pos+3:]

class Response():
    def __init__(self):
        self.code = 200
        self.headers = {"Content-Type":"text/html"}
        self.body = ""
    
    def set_header(self, name, value):
        self.headers.update({name:value})
    
    def create(self):
        # Status line
        response = "HTTP/1.1 " + str(self.code) + " " + str(response_codes[self.code]) + "\r\n"

        # Headers
        for key in self.headers.keys():
            response += key + ":" + self.headers[key] + "\r\n"

        # Body
        response += "\r\n" + self.body

        return response
    
    def render_template(self, html_file, elements = {}):
        try:
            page = open(html_file, "r")
        except FileNotFoundError:
            return ""
        
        body = page.read()

        for key in elements.keys():
            body = body.replace("{" + key + "}", str(elements[key]))

        return body
