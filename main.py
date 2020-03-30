import usocket
import sys
import httplib
import light
import pages
import _thread
import ujson
import time

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

        # API -------------------------------------------------------------------------------------
        elif "/api/" in link:
            api = link.split("/api/")[1]
            if api == "ledon":
                _thread.start_new_thread(light.on, ())
                httplib.SendResponse(client, "application/json", """{"status":"ON"}""")
            elif api == "ledoff":
                _thread.start_new_thread(light.off, ())
                httplib.SendResponse(client, "application/json", """{"status":"OFF"}""")
            elif api == "status":
                httplib.SendResponse(client, "application/json", 
                    "{{\"status\":\"{}\",\"previous_on\":{}, \"current_on\":{}}}".format(
                        light.status,
                        light.previous_on,
                        int(time.time() - light.current_on) if light.current_on > 0 else 0))
            elif api == "settings":
                httplib.SendResponse(client, "application/json", open("data/settings.json","r").read())
            else:
                httplib.SendResponse(client, "application/json", """{"error":"not defined"}""")

        else:
            httplib.SendError(client, 404,"Not found")

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
            settings_file = open("data/settings.json","w")
            ujson.dump(settings, settings_file)
            settings_file.close()
            
            httplib.SendResponse(client, "text/html", pages.settings())
        
        elif link == "/connection":
            # Split body to dictionary
            body = body.split("&")
            temp = []
            for element in body: temp.extend(element.split("="))
            connection = {temp[i]:temp[i+1] for i in range(0,len(temp),2)}
            # Save to file
            connection_file = open("data/connection.json","w")
            ujson.dump(connection, connection_file)
            connection_file.close()
            
            httplib.SendResponse(client, "text/html", pages.connection())

        # API -------------------------------------------------------------------------------------
        elif "/api/" in link:
            api = link.split("/api/")[1]
            httplib.SendResponse(client, "application/json", """{"error":"not defined"}""")
        
        else:
            httplib.SendError(client, 404,"Not found")

    client.close()
