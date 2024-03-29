import usocket
import sys
import time
import gc

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
        self.debug_on = False

    def run(self, port = 80):
        self._port = port

        # Create http server
        server = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
        try:
            server.bind(('', self._port))
        except:
            self._debug_msg(["localhost",self._port],"Bind failed.")
            sys.exit()
        server.listen(5)

        while True:
            client, addr = server.accept()
            self._debug_msg(addr,"Connected")

            # When no data received, raise exception
            client.settimeout(0.5)
            try:
                data = client.recv(1024)
            except:
                client.close()
                self._debug_msg(addr,"No request. Disconnected")
                continue
            
            # Parse received data
            self.request.parse(data)
            self._debug_msg(addr, "Method:  " + self.request.method)
            self._debug_msg(addr, "Url:     " + self.request.url)
            self._debug_msg(addr, "Query:   " + str(self.request.query))
            self._debug_msg(addr, "Headers: " + str(self.request.headers))
            self._debug_msg(addr, "Content: " + str(self.request.content))

            # Call routed funtion
            try:
                self.response.body = self._route_functions[self.request.url](**self.request.query)
            except KeyError as err:
                client.sendall(self.response.error(self.request, "Unknown URL", str(err)))
                client.close()
                self._debug_msg(addr,"Unknown url. Disconnected. ERROR: "+ str(err))
                continue

            # Send response
            client.sendall(self.response.create())
            client.close()
            self._debug_msg(addr, "Disconnected")

            # Set headers to default
            self.response.headers = {"Content-Type":"text/html"}
            gc.collect()

    def route(self, url):
        def wrap(f):
            self._route_functions[url] = f
            return f
        return wrap

    def _debug_msg(self, address, message):
        if self.debug_on:
            print("[{:10d}|{}:{}]: {}".format(time.ticks_ms(), address[0], address[1], message))

class Request():
    def __init__(self):
        self.method = ""
        self.url = ""
        self.version = ""
        self.headers = {}
        self.content = ""
        self.query = {}

    def parse(self, data):
        # Set to default
        self.method = ""
        self.url = ""
        self.version = ""
        self.headers = {}
        self.content = ""
        self.query = {}

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

        # URL Query
        if "?" in self.url:
            temp = self.url.split("?")
            self.url = temp[0]              # url without query
            queries = temp[1].split("&")    # queries
            
            for query in queries:
                key, value = query.split("=")
                self.query.update({key:value})

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
        
        template = page.read()

        for key in elements.keys():
            template = template.replace("{{" + key + "}}", str(elements[key]))

        return template

    def error(self, request, errorname, message):
        self.code = 404
        self.body = """
        <style>
            div {background-color: rgb(255, 144, 144); border: 1px; border-radius: 4px; max-width: 600px; padding: 20px; margin: 10px auto; font-size: 1em; text-align: center}
            .message {background-color: rgb(144, 144, 144);}
            table {border-collapse: collapse; width: 100%;}
            td, th {border: 1px solid; text-align: left; padding: 4px;}
            .value {font-style: italic;}
        </style>
        <div>
            <H2> ERROR: """ + errorname + """</H2>
        </div>
        <div class="message">
            <table>
                <tr>
                    <th>Method</th>
                    <th class="value">"""+ request.method +"""</th>
                </tr>
                <tr>
                    <th>URL</th>
                    <th class="value">"""+ request.url +"""</th>
                </tr>
                <tr>
                    <th>Content</th>
                    <th class="value">"""+ str(request.content) +"""</th>
                </tr>
                <tr>
                    <th>Error message</th>
                    <th class="value">"""+ message +"""</th>
                </tr>
        </div>
        """
        return self.create()
