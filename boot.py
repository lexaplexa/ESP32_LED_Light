import gc
gc.collect()

import network
import ujson

connection = ujson.load(open("connection.json","r"))

if connection["WifiMode"] == "STATION":

    st = network.WLAN(network.STA_IF)
    st.active(True)
    st.connect(connection["ssid"], connection["password"])

    while st.isconnected() == False:
        pass
    
    print("Connected to " + connection["ssid"])
    print(st.ifconfig())

else:
    ap = network.WLAN(network.AP_IF)
    ap.config(essid=connection["ssid"])
    ap.active(True)
    
    print("AP established")
    print (ap.ifconfig())