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
        settings["Name"]    = app.request.content["Name"]
        settings["Timeout"] = int(app.request.content["Timeout"])
        settings["Max"]     = int(app.request.content["Max"])
        settings["Rise"]    = int(app.request.content["Rise"])
        settings["Fall"]    = int(app.request.content["Fall"])
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

# Here starts application
if __name__ == "__main__":
    app.debug_on = True
    app.run()
