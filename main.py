import usocket
import sys
import httplib
import light
import pages
import _thread
import ujson

# Create web server
server = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
try:
    server.bind(('', 80))
except:
    print('# Bind failed. ')
    sys.exit()
server.listen(5)

while True:
    client, addr = server.accept()
    print("Connected to "+str(addr[0])+":"+str(addr[1]))
    
    # Handle client request -----------------------------------------------------------------------
    try:
        method, link, body = httplib.GetRequest(client)
    except:
        client.close()
        print("Client disconnected")
        continue

    # GET method ----------------------------------------------------------------------------------
    if method == "GET":
        if link == "/":
            httplib.SendResponse(client, "text/html", pages.index(light.status))

        elif link == "/?led=on":
            _thread.start_new_thread(light.on,())
            httplib.SendResponse(client, "text/html", pages.index("ON"))
        
        elif link == "/?led=off":
            _thread.start_new_thread(light.off,())
            httplib.SendResponse(client, "text/html", pages.index("OFF"))

        elif link == "/settings":
            httplib.SendResponse(client, "text/html", pages.settings())
        
        elif link == "/connection":
            httplib.SendResponse(client, "text/html", pages.connection())

        else:
            httplib.SendError(client, 404,"Not found")
        pass
    
    # POST method ---------------------------------------------------------------------------------
    elif method == "POST":
        if link == "/settings":
            # Split body to dictionary
            body = body.split("&")
            temp = []
            for element in body: temp.extend(element.split("="))
            settings = {temp[i]:temp[i+1] for i in range(0,len(temp),2)}
            # Convert to integer
            settings["Max"] = int(settings["Max"])
            settings["Timeout"] = int(settings["Timeout"])
            settings["Rise"] = int(settings["Rise"])
            settings["Fall"] = int(settings["Fall"])
            # Save to file
            settings_file = open("settings.json","w")
            ujson.dump(settings, settings_file)
            settings_file.close()
            
            httplib.SendResponse(client, "text/html", pages.settings())

    client.close()
