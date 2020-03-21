def GetRequest(client):
    # When no data received, raise exception
    client.settimeout(0.2)

    # Wait for data from client
    data = ConvertToUtf8(client.recv(1024))
    
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

def ConvertToUtf8(data):
    # Convert UTF-8 characters to bytes
    # Example: "%C3%BD" >> b'\xc3\xbd'
    while(1):
        pos = data.find(b'%')
        if pos == -1:
            return data
        data = data[:pos]+bytes([int(data[pos+1:pos+3],16)])+data[pos+3:]
