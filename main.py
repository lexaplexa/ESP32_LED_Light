from httplib import Http
import ujson
import light

app = Http()

@app.route("/")
def index():
    settings = ujson.load(open("data/settings.json","r"))
    elements = {"style": open("html/style.css","r").read(),"room":settings["Name"]}

    if light.status == "ON":
        elements.update({"class_div_light":"lighton"})
    else:
        elements.update({"class_div_light":"lightoff"})

    return app.response.render_template("html/index.html", elements)

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

    elements = {
        "style":            open("html/style.css","r").read(),
        "room":             settings["Name"],
        "settings_name":    settings["Name"],
        "settings_timeout": settings["Timeout"],
        "settings_max":     settings["Max"],
        "settings_rise":    settings["Rise"],
        "settings_fall":    settings["Fall"]}
    return app.response.render_template("html/settings.html", elements)

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

    elements = {
        "style":            open("html/style.css","r").read(),
        "room":             settings["Name"],
        "connection_ssid":  connection["ssid"]}
    if connection["WifiMode"] == "AP":
        elements.update({"select_ap":"selected"})
        elements.update({"select_st":""})
    else:
        elements.update({"select_ap":""})
        elements.update({"select_st":"selected"})
    return app.response.render_template("html/connection.html", elements)


# Here starts application
if __name__ == "__main__":
    app.debug_on = True
    app.run()
