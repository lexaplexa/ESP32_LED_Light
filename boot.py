import gc
gc.collect()

import network
import ujson

connection = ujson.load(open("data/connection.json","r"))

if connection["connection_wifimode"] == "STATION":

    st = network.WLAN(network.STA_IF)
    st.active(True)
    st.connect(connection["connection_ssid"], connection["connection_password"])

    while st.isconnected() == False:
        pass
    
    print("Connected to " + connection["connection_ssid"])
    print(st.ifconfig())

else:
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid=connection["connection_ssid"], password=connection["connection_password"])
    
    print("AP established")
    print (ap.ifconfig())