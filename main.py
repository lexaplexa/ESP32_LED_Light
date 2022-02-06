from httplib import Http
import ujson
import light
import _thread
import ubinascii
import network

app = Http()

@app.route("/")
def index(status = ""):
    settings = ujson.load(open("data/settings.json","r"))
    settings.update({"style":open("html/style.css","r").read()})
    settings.update({"img_power_button": ubinascii.b2a_base64(open("/img/power-button.png").read()).decode("utf-8")})

    if status == "on":
        light.status = "ON"
        _thread.start_new_thread(light.on, ())
    elif status == "off":
        light.status = "OFF"
        _thread.start_new_thread(light.off, ())
    
    if light.status == "ON":
        settings.update({"class_div_light":"lighton"})
    else:
        settings.update({"class_div_light":"lightoff"})

    return app.response.render_template("html/index.html", settings)

@app.route("/settings")
def settings():
    settings = ujson.load(open("data/settings.json","r"))
    if app.request.method == "POST":
        settings = {}
        for key in app.request.content.keys():
            if app.request.content[key].isdigit():
                settings.update({key:int(app.request.content[key])})
            else:
                settings.update({key:app.request.content[key]})
        settings_file = open("data/settings.json","w")
        ujson.dump(settings, settings_file)
        settings_file.close()

    settings.update({"style":open("html/style.css","r").read()})
    return app.response.render_template("html/settings.html", settings)

@app.route("/connection")
def connection():
    settings = ujson.load(open("data/settings.json","r"))
    connection = ujson.load(open("data/connection.json","r"))
    if app.request.method == "POST":
        connection = {}
        for key in app.request.content.keys():
            connection.update({key:app.request.content[key]})
        connection_file = open("data/connection.json","w")
        ujson.dump(connection, connection_file)
        connection_file.close()

    elements = {}
    elements.update(settings)
    elements.update(connection)
    if connection["connection_wifimode"] == "AP":
        elements.update({"connection_select_ap":"selected"})
        elements.update({"connection_select_st":""})
    else:
        elements.update({"connection_select_ap":""})
        elements.update({"connection_select_st":"selected"})
    elements.update({"style":open("html/style.css","r").read()})
    return app.response.render_template("html/connection.html", elements)


# Here starts application
if __name__ == "__main__":
    app.debug_on = True
    app.run()
