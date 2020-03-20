import ujson

html_template = """
<html>
<head>
    {head}
<style>
    {style}
</style>
</head>
<body>
    {body}
</body>
<script>
    {script}
</script>
</html>"""

style = """html{background-color: black; font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
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
    
    select {font-size: 1em; width: 200px;}"""

def index(light_status):
    settings = ujson.load(open("settings.json","r"))

    if light_status == "OFF":
        div_light = "lightoff"
    else:
        div_light = "lighton"

    head = """
    <title>Světlo | """ + settings["Name"] + """</title>
    <meta name="viewport" content="width=device-width, initial-scale=1" charset="UTF-8">
    <link rel="icon" href="data:,">"""
    body = """
    <a href="/">
      <div class="title">
        <h1>Světlo | """ + settings["Name"] + """</h1>
      </div>
    </a>
    <div class=""" + div_light + """>
      <a href="/?led=on"><button class="on">Rožni</button></a>
      <a href="/?led=off"><button class="off">Zhasni</button></a>
    </div>
    <div class="buttons">
      <a href="/settings"><button class="settings">Parametry</button></a>
      <a href="/connection"><button class="settings">Wifi</button></a>
    </div>"""

    html = html_template
    html = html.replace("{head}",head)
    html = html.replace("{style}",style)
    html = html.replace("{body}",body)
    html = html.replace("{script}","")

    return html

def settings():
    settings = ujson.load(open("settings.json","r"))

    head = """
    <title>Světlo | """ + settings["Name"] + """</title>
    <meta name="viewport" content="width=device-width, initial-scale=1" charset="UTF-8">
    <link rel="icon" href="data:,">"""
    body = """
    <a href="/"><div class="title">
      <h1>Světlo | """ + settings["Name"] + """</h1>
    </div></a>
    <form name="settings" action="/settings" method="post">
      <div>
        Jméno<br><br>
        <input id="Name" name="Name" type="Text" value=""" + str(settings["Name"]) + """ class="name">
      </div>
      <div>
        Automatické zhasnutí<br><br>
        <input id="Timeout" name="Timeout" type="Number" value=""" + str(settings["Timeout"]) + """ class="timeout"> minut
      </div>
      <div>
        Jas
        <p><span id="MaxSliderVal"></span>%</p>
        <input id="MaxSlider" name="Max" type="range" min=1 max=100 value=""" + str(settings["Max"]) + """ class="slider">            
      </div>
      <div>
        Doba zapínání
        <p><span id="RiseSliderVal"></span></p>
        <input id="RiseSlider" name="Rise" type="range" min=1 max=20 value=""" + str(settings["Rise"]) + """ class="slider">
      </div>
      <div>
        Doba vypínání
        <p><span id="FallSliderVal"></span></p>
        <input id="FallSlider" name="Fall" type="range" min=1 max=20 value=""" + str(settings["Fall"]) + """ class="slider">
      </div>
      <div class="buttons">
        <input type="submit" value="Uložit" class="submit">
      </div>
    </form>"""
    script = """
    document.getElementById("MaxSliderVal").innerHTML = document.getElementById("MaxSlider").value;
    document.getElementById("RiseSliderVal").innerHTML = document.getElementById("RiseSlider").value;
    document.getElementById("FallSliderVal").innerHTML = document.getElementById("FallSlider").value;

    document.getElementById("MaxSlider").oninput = function() {document.getElementById("MaxSliderVal").innerHTML = this.value;}
    document.getElementById("RiseSlider").oninput = function() {document.getElementById("RiseSliderVal").innerHTML = this.value;}
    document.getElementById("FallSlider").oninput = function() {document.getElementById("FallSliderVal").innerHTML = this.value;}"""

    html = html_template
    html = html.replace("{head}",head)
    html = html.replace("{style}",style)
    html = html.replace("{body}",body)
    html = html.replace("{script}",script)

    return html

def connection():
    settings = ujson.load(open("settings.json","r"))
    connection = ujson.load(open("connection.json","r"))

    if connection["WifiMode"] == "STATION":
        sel_ap = ""
        sel_st = "selected"
    else:
        sel_ap = "selected"
        sel_st = ""

    head = """
    <title>Světlo | """ + settings["Name"] + """</title>
    <meta name="viewport" content="width=device-width, initial-scale=1" charset="UTF-8">
    <link rel="icon" href="data:,">"""
    body = """
    <a href="/"><div class="title">
      <h1>Světlo | """ + settings["Name"] + """</h1>
    </div></a>
    <form name="connection" action="/connection" method="post">
      <div>
        Mód WIFI<br><br>
        <select name="WifiMode">
          <option value="AP" """ + sel_ap + """>AP</option>
          <option value="STATION" """ + sel_st + """>STATION</option>
        </select>
      </div>
      <div>
        SSID<br><br>
        <input name="ssid" type="Text" value=""" + str(connection["ssid"]) + """ class="name">
      </div>
      <div>
        Heslo<br><br>
        <input name="password" type="password" class="name">
      </div>
      <div class="buttons">
        <input type="submit" value="Uložit" class="submit">
      </div>
    </form>"""

    html = html_template
    html = html.replace("{head}",head)
    html = html.replace("{style}",style)
    html = html.replace("{body}",body)
    html = html.replace("{script}","")

    return html