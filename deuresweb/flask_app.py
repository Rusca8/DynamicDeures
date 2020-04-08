
# A very simple Flask Hello World app for you to get started with...

from flask import Flask
from flask import redirect, render_template, request
import latexator as g
import telegramor as tele
import exemplesindex as e

app = Flask(__name__, template_folder="templates/")


@app.route('/')
def index():
    return render_template("index.html", ex=e.genera())


@app.route('/ex')
def indexvar():
    return render_template("index.html", ex=e.genera(True))


@app.route("/equacions/", methods=["GET", "POST"])
def equacions():
    if request.method == "POST":

        g.equacions(request.form, solucions=False)  # genera el pdf amb latex

        tele.feedback("eq", request.form)
        return redirect("/pdf/eq")
    else:
        return render_template("equacions.html",textbotgen="Generar fitxa!")


@app.route("/enters/", methods=["GET", "POST"])
def combinades():
    if request.method == "POST":
        try:
            g.combinades(request.form, solucions=False)
        except:
            return redirect("/latex_error/combinades")

        tele.feedback("comb",request.form)
        return redirect("/pdf/comb")
    else:
        return render_template("combinades.html")


@app.route("/apilades/", methods=["GET", "POST"])
def apilades():
    if request.method == "POST":
        try:
            g.apilades(request.form, solucions=False)
        except:
            return redirect("/latex_error/apilades")

        tele.feedback("api",request.form)
        return redirect("/pdf/apilades")
    else:
        return render_template("apilades.html")


@app.route("/proporcionalitat/", methods=["GET", "POST"])
def proporcionalitat():
    if request.method == "POST":
        try:
            g.proporcionalitat(request.form, solucions=False)
        except:
            return redirect("/latex_error/proporcionalitat")

        tele.feedback("prop",request.form)
        return redirect("/pdf/proporcionalitat")
    else:
        return render_template("proporcionalitat.html")


@app.route("/proves/", methods=["GET", "POST"])
def proves():
    if request.method == "POST":
        print(request.form)
        g.proporcionalitat(request.form, solucions=False)
        return redirect("/pdf/proporcionalitat")
    else:
        return render_template("proporcionalitat.html")


@app.route("/provaforms/", methods=["GET", "POST"])
def provaforms():
    if request.method == "POST":
        form = request.form
        return render_template("provaforms.html", form=form, post=True)
    else:
        return render_template("provaforms.html")


@app.route('/pdf/<tema>')
def pdfviewer(tema):
    print(f"Visualitzant pdf: {tema}.")
    if tema == "eq":
        return redirect("/static/pdfs/equacions.pdf")
    elif tema == "comb":
        return redirect("/static/pdfs/combinades.pdf")
    elif tema == "proves":
        return redirect("/static/pdfs/proves.pdf")
    elif tema == "apilades":
        return redirect("/static/pdfs/apilades.pdf")
    elif tema == "proporcionalitat":
        return redirect("/static/pdfs/proporcionalitat.pdf")
    else:
        return f"No s'ha trobat el pdf {tema}"


@app.route("/com/")
def com():
    return render_template("com.html")


@app.route("/canvis/")
def canvis():
    return render_template("changelog.html")


@app.route('/latex_error/<pdf>')
def latexerror(pdf):
    return f"<h2>Hi ha hagut algun problema greu fent el teu pdf de {pdf}</h2><p>...o potser algú ha tingut l'error abans i ha quedat caigut, que també em passa</p>"


@app.route('/<patillada>')
def notfound(patillada):
    return f"<h1>404</h1><br><h2>la pàgina {patillada} no existeix </h2>"


if __name__ == "__main__":  # això la fa córrer en local
    app.run()