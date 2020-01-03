import usocket as socket
import sys

def CreateServer(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind(('', port))
    except:
        print('# Bind failed. ')
        sys.exit()
    server.listen(5)
    return server

def GetRequest(client):
    # When no data received, raise exception
    client.settimeout(0.2)

    # Wait for data from client
    data = client.recv(1024)
    
    # Separate http header from body
    header = data.decode('utf-8').split("\r\n\r\n")[0]
    header = header.split("\n")
    try:
        method, link, html = header[0].split()
    except:
        return None, None, None

    body = data.decode('utf-8').split("\r\n\r\n")[1]
    print("Method: "+method+"\nLink: "+link+"\nBody: "+body)
    return method, link, body

def SendResponse(client, content_type, string):
    response = "HTTP/1.1 200 OK\nContent-Type: "+ content_type +"\nConnection: close\n\n" + string
    client.sendall(response)
    return

def SendError(client, error_number, message):
    response = "HTTP/1.1 {} \nContent-Type: text/html\nConnection: close\n\n<H1>{} {}</H1>".format(error_number,error_number,message)
    client.sendall(response)
    client.close()
    return