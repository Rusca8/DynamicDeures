import urllib.request
from latexator import tematitol, temallarg
from teletoken import gettoken

import urllib.parse


def feedback(tema, opcions):
    teletexto = "S'han generat exercicis *" + tematitol(tema) + "* _(" + opcions["curs"] + ")_ "
    teletexto = urllib.parse.quote_plus(teletexto)
    bottoken = gettoken()
    if gettoken() == "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11":
        print("utilitzant el token de prova")
    else:
        url = ("https://api.telegram.org/bot" + bottoken
               + "/sendMessage?chat_id=@ddfeedback&disable_notification=true&text=" + teletexto
               + "&parse_mode=Markdown")
        with urllib.request.urlopen(url) as x:
            x.read()


def error(tema):
    teletexto = "⚠️ *Error* (" + temallarg(tema) + ")"
    teletexto = urllib.parse.quote_plus(teletexto)
    bottoken = gettoken()
    if gettoken() == "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11":
        print("utilitzant el token de prova")
    else:
        url = ("https://api.telegram.org/bot" + bottoken
               + "/sendMessage?chat_id=@ddfeedback&disable_notification=true&text=" + teletexto
               + "&parse_mode=Markdown")
        with urllib.request.urlopen(url) as x:
            x.read()