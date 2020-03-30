import ujson

def replace_value(html, bracket_name, value):
    return html.replace("{" + bracket_name + "}", value)

style = """
    html{background-color: black; font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}

    a:link, a:visited, a:active, a:hover {text-decoration: none; color: white;}

    button {display: inline-block; border: 1px; border-radius: 4px; border-style: solid; padding: 16px 40px; text-decoration: none; font-weight:bold; font-size: 1em; margin: 5px; cursor: pointer;}
    .on {background-color: orange; color: white;}
    .off {background-color: gray; color: black;}
    .settings {background-color: lightblue; color: white;}

    input {text-align: center; font-size: 1em;}
    .slider {-webkit-appearance: none; width: 60%; height: 15px; border-radius: 5px; background: #d3d3d3; outline: none;}
    .name {width: 200px;}
    .timeout {width: 80px;}
    .submit {background-color: lightblue; border: 1px; border-radius: 4px; border-style: solid; color: white; padding: 16px 40px; text-decoration: none; margin: 5px; cursor: pointer; font-weight:bold;}

    div {background-color: #EAEAEA; border: 1px; border-radius: 4px; max-width: 600px; padding: 20px; margin: 10px auto; font-size: 1.5em;}
    .title {background-color: green; font-size: 1em;}
    .lighton {background-color: orange; color: white;}
    .lightoff {background-color: gray; color: black;}
    .buttons {display: flex; justify-content: center;}

    select {font-size: 1em; width: 200px;}

    hr {color: white; max-width: 640px;}

    footer {color: white; bold}"""

def index(light_status):
    # Load html file and settings first
    html = open("html/index.html","r").read()
    settings = ujson.load(open("data/settings.json","r"))

    # Replace all values in brackets {} with real values
    html = replace_value(html, "room", settings["Name"])
    html = replace_value(html, "style", style)

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
    html = replace_value(html, "style", style)
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
    html = replace_value(html, "style", style)
    html = replace_value(html, "connection_ssid", connection["ssid"])

    if connection["WifiMode"] == "STATION":
        html = replace_value(html, "select_ap", "")
        html = replace_value(html, "select_st", "selected")
    else:
        html = replace_value(html, "select_ap", "selected")
        html = replace_value(html, "select_st", "")

    return html