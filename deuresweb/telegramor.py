import urllib.request
from latexator import tematitol
from teletoken import gettoken

import urllib.parse

def feedback(tema, opcions):
    telegramText = "S'han generat exercicis *" + tematitol(tema) + "* _(" + opcions["curs"] + ")_ "
    telegramText = urllib.parse.quote_plus(telegramText)
    botToken = gettoken()
    if gettoken() == "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11":
        print("utilitzant el token de prova")
    else:
        url = "https://api.telegram.org/bot" + botToken \
              + "/sendMessage?chat_id=@ddfeedback&disable_notification=true&text=" + telegramText \
              + "&parse_mode=Markdown"
        with urllib.request.urlopen(url) as x:
            x.read()
