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

style = """html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center; background-color: black;}
          a:link, a:visited, a:active, a:hover {text-decoration: none; color: white;}
          p{font-size: 1.5em;}
          .button{display: inline-block; border: none; border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
          .button_on{background-color: orange;}
          .button_off{background-color: gray; color: black;}
          .button_settings{background-color: lightblue;}
          input {text-align: center; font-size: 1.2em;}
          .slider {-webkit-appearance: none; width: 60%; height: 15px; border-radius: 5px; background: #d3d3d3; outline: none;}
          .name {width: 200px;}
          .timeout {width: 80px;}
          div {background-color: #EAEAEA; border: 1px; border-radius: 4px; max-width:600px; padding: 20px; margin: 10px auto;}
          .title {background-color: green;}
          .lighton {background-color: orange; color: white;}
          .lightoff {background-color: gray; color: black;}"""

def index(light_status):
    if light_status == "OFF":
        status = "ZHASNUTO"
        div_light = "lightoff"
    else:
        status = "ROŽNUTO"
        div_light = "lighton"

    settings = ujson.load(open("settings.json","r"))

    html = html_template
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
        <div class= """ + div_light + """>
            <p><strong>""" + status + """</strong></p>
        </div>
        <div>
          <p><a href="/?led=on"><button class="button button_on">Rožni</button></a></p>
          <p><a href="/?led=off"><button class="button button_off">Zhasni</button></a></p>
        </div>
        <p><a href="/settings"><button class="button button_settings">Nastavení</button></a></p>"""

    html = html.replace("{head}",head)
    html = html.replace("{style}",style)
    html = html.replace("{body}",body)
    html = html.replace("{script}","")

    return html

def settings():
    settings = ujson.load(open("settings.json","r"))

    html = html_template
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
            <p>Jméno</p>
            <input id="Name" name="Name" type="Text" value=""" + str(settings["Name"]) + """ class="name">
          </div>
          <div>
            <p>Automatické zhasnutí</p>
            <input id="Timeout" name="Timeout" type="Number" value=""" + str(settings["Timeout"]) + """ class="timeout"> minut
          </div>
          <div>
            <p>Jas</p>
            <p><span id="MaxSliderVal"></span>%</p>
            <input id="MaxSlider" name="Max" type="range" min=1 max=100 value=""" + str(settings["Max"]) + """ class="slider">            
          </div>
          <div>
            <p>Doba zapínání</p>
            <p><span id="RiseSliderVal"></span></p>
            <input id="RiseSlider" name="Rise" type="range" min=1 max=20 value=""" + str(settings["Rise"]) + """ class="slider">
          </div>
          <div>
            <p>Doba vypínání</p>
            <p><span id="FallSliderVal"></span></p>
            <input id="FallSlider" name="Fall" type="range" min=1 max=20 value=""" + str(settings["Fall"]) + """ class="slider">
          </div>
          <br>
          <input type="submit" value="Uložit" class="button button_settings">
        </form>"""
    script = """
        document.getElementById("MaxSliderVal").innerHTML = document.getElementById("MaxSlider").value;
        document.getElementById("RiseSliderVal").innerHTML = document.getElementById("RiseSlider").value;
        document.getElementById("FallSliderVal").innerHTML = document.getElementById("FallSlider").value;

        document.getElementById("MaxSlider").oninput = function() {document.getElementById("MaxSliderVal").innerHTML = this.value;}
        document.getElementById("RiseSlider").oninput = function() {document.getElementById("RiseSliderVal").innerHTML = this.value;}
        document.getElementById("FallSlider").oninput = function() {document.getElementById("FallSliderVal").innerHTML = this.value;}"""

    html = html.replace("{head}",head)
    html = html.replace("{style}",style)
    html = html.replace("{body}",body)
    html = html.replace("{script}",script)

    return html