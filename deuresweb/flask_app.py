
# A very simple Flask Hello World app for you to get started with...

from flask import Flask
from flask import redirect, render_template, request
import latexator as g
import telegramor as tele
import exemplesindex as e

app = Flask(__name__, template_folder="templates/")


@app.route('/')
def index():
    #try:
    return render_template("index.html", ex=e.genera())
    #except:
    #    return f"<h1>Ui</h1><h2>Hi ha hagut algun problema carregant la pàgina.</h2><p>Si es manté avisa'm! (Twitter: @Rusca8 | Insta: @drusca8 | Mail: rusca.dev@gmail.com)</p>"


@app.route('/ex/')
def indexvar():
    try:
        return render_template("index.html", ex=e.genera(True))
    except:
        return f"<h1>Ui</h1><h2>Hi ha hagut algun problema carregant la pàgina.</h2><p>Si es manté avisa'm! (Twitter: @Rusca8 | Insta: @drusca8 | Mail: rusca.dev@gmail.com)</p>"


@app.route("/equacions/", methods=["GET", "POST"])
def equacions():
    if request.method == "POST":
        try:
            g.equacions(request.form, solucions=False)  # genera el pdf amb latex
        except:
            return redirect("/latex_error/equacions")
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

        tele.feedback("comb", request.form)
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

        tele.feedback("api", request.form)
        return redirect("/pdf/apilades")
    else:
        return render_template("apilades.html")


@app.route("/powsqr/", methods=["GET", "POST"])
def powsqr():
    if request.method == "POST":
        try:
            g.powsqr(request.form, solucions=False)
        except:
            return redirect("/latex_error/apilades")

        tele.feedback("powsqr", request.form)
        return redirect("/pdf/powsqr")
    else:
        return render_template("powsqr.html")


@app.route("/fraccions/", methods=["GET", "POST"])
def fraccions():
    if request.method == "POST":
        try:
            g.fraccions(request.form, solucions=False)
        except:
            return redirect("/latex_error/fraccions")
        tele.feedback("frac", request.form)
        return redirect("/pdf/fraccions")
    else:
        return render_template("fraccions.html")


@app.route("/proporcionalitat/", methods=["GET", "POST"])
def proporcionalitat():
    if request.method == "POST":
        try:
            g.proporcionalitat(request.form, solucions=False)
        except:
            return redirect("/latex_error/proporcionalitat")

        tele.feedback("prop", request.form)
        return redirect("/pdf/proporcionalitat")
    else:
        return render_template("proporcionalitat.html")


@app.route("/success/", methods=["GET", "POST"])
def success():
    if request.method == "POST":
        try:
            g.successions(request.form, solucions=False)
        except:
            return redirect("/latex_error/successions")
        tele.feedback("succ", request.form)
        return redirect("/pdf/successions")
    else:
        return render_template("successions.html")


@app.route("/derivades/", methods=["GET", "POST"])
def derivades():
    if request.method == "POST":
        try:
            g.derivades(request.form, solucions=False)
        except:
            return redirect("/latex_error/derivades")
        tele.feedback("dx", request.form)
        return redirect("/pdf/derivades")
    else:
        return render_template("derivades.html")


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
    elif tema == "powsqr":
        return redirect("/static/pdfs/powsqr.pdf")
    elif tema == "fraccions":
        return redirect("/static/pdfs/fraccions.pdf")
    elif tema == "proporcionalitat":
        return redirect("/static/pdfs/proporcionalitat.pdf")
    elif tema == "successions":
        return redirect("/static/pdfs/successions.pdf")
    elif tema == "derivades":
        return redirect("/static/pdfs/derivades.pdf")
    else:
        return f"No s'ha trobat el pdf {tema}"


@app.route("/com/")
def com():
    return render_template("com.html")


@app.route("/canvis/")
def canvis():
    return render_template("changelog.html")


@app.route("/contacte/")
def contacte():
    return render_template("contacte.html")


@app.route('/latex_error/<pdf>')
def latexerror(pdf):
    return f"<h2>Hi ha hagut algun problema greu fent el teu pdf de {pdf}</h2><p>...o potser algú ha tingut l'error abans i ha quedat caigut, que també em passa</p>"


@app.route('/<patillada>')
def notfound(patillada):
    return f"<h1>404</h1><br><h2>la pàgina {patillada} no existeix </h2>"


if __name__ == "__main__":  # això la fa córrer en local
    app.run(debug=True)
