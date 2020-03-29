import ujson

def replace_value(html, bracket_name, value):
    return html.replace("{" + bracket_name + "}", value)

def index(light_status):
    # Load html file and settings first
    html = open("html/index.html","r").read()
    settings = ujson.load(open("data/settings.json","r"))

    # Replace all values in brackets {} with real values
    html = replace_value(html, "room", settings["Name"])

    if light_status == "OFF":
        html = replace_value(html, "class_div_light", "lightoff")
    else:
        html = replace_value(html, "class_div_light", "lighton")

    return html

def settings():
    # Load html file and settings first
    html = open("html/settings.html","r").read()
    settings = ujson.load(open("data/settings.json","r"))

    # Replace all values in brackets {} with real values
    html = replace_value(html, "room", settings["Name"])
    html = replace_value(html, "settings_name", settings["Name"])
    html = replace_value(html, "settings_timeout", str(settings["Timeout"]))
    html = replace_value(html, "settings_max", str(settings["Max"]))
    html = replace_value(html, "settings_rise", str(settings["Rise"]))
    html = replace_value(html, "settings_fall", str(settings["Fall"]))

    return html

def connection():
    # Load html file, settings and connection first
    html = open("html/connection.html","r").read()
    settings = ujson.load(open("data/settings.json","r"))
    connection = ujson.load(open("data/connection.json","r"))

    # Replace all values in brackets {} with real values
    html = replace_value(html, "room", settings["Name"])
    html = replace_value(html, "connection_ssid", connection["ssid"])

    if connection["WifiMode"] == "STATION":
        html = replace_value(html, "select_ap", "")
        html = replace_value(html, "select_st", "selected")
    else:
        html = replace_value(html, "select_ap", "selected")
        html = replace_value(html, "select_st", "")

    return html