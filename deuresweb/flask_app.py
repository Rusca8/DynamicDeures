
# A very simple Flask Hello World app for you to get started with...

from flask import Flask
from flask import redirect, render_template, request

import os

import latexator as g
import telegramor as tele
import exemplesindex as e

from puntuacions import punts_de
from quantitats import quantitats_de
from noms import nom_apartat, nom_tema

app = Flask(__name__, template_folder="templates/")
app.jinja_env.add_extension('jinja2.ext.do')


@app.context_processor
def ctx():
    return dict(punts=punts_de,
                quantitats=quantitats_de,
                nom_apartat=nom_apartat,
                nom_tema=nom_tema,
                os=os,  # per saber si els fitxers existeixen des de jinja: os.path.exists('path')
                )


@app.route('/')
def index():
    try:
        return render_template("index.html", ex=e.genera())
    except:
        return (f"<h1>Ui</h1><h2>Hi ha hagut algun problema carregant la pàgina.</h2>"
                f"<p>Si es manté avisa'm! (Twitter: @Rusca8 | Insta: @drusca8 | Mail: dynamicdeures@gmail.com)</p>")


@app.route('/q/')
def q_index():
    try:
        return render_template("q_index.html")
    except:
        return (f"<h1>Ui</h1><h2>Hi ha hagut algun problema carregant la pàgina.</h2>"
                f"<p>Si es manté avisa'm! (Twitter: @Rusca8 | Insta: @drusca8 | Mail: dynamicdeures@gmail.com)</p>")


@app.route('/ex/')
def indexvar():
    """return render_template("index.html", ex=e.genera(True))
    """
    try:
        return render_template("index.html", ex=e.genera(True))
    except:
        return (f"<h1>Ui</h1><h2>Hi ha hagut algun problema carregant la pàgina.</h2>"
                f"<p>Si es manté avisa'm! (Twitter: @Rusca8 | Insta: @drusca8 | Mail: dynamicdeures@gmail.com)</p>")


@app.route("/equacions/", methods=["GET", "POST"])
def equacions():
    if request.method == "POST":
        if app.debug:
            print("(Debug mode on...)")
            url = g.crea_fitxa(request.form)
        else:
            try:
                url = g.crea_fitxa(request.form)
            except Exception as exc:
                print(f"Error Equacions ({exc})")
                tele.error("eq")
                return redirect("/latex_error/equacions")
            tele.feedback("eq", request.form)
        return redirect(url)
    else:
        return render_template("equacions.html")


@app.route("/enters/", methods=["GET", "POST"])
def combinades():
    if request.method == "POST":
        """g.combinades(request.form, solucions=False)
        """
        try:
            g.combinades(request.form)
        except:
            print("Error Combinades")
            tele.error("comb")
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
            print("Error Apilades")
            tele.error("api")
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
            print("Error Potències")
            tele.error("powsqr")
            return redirect("/latex_error/powsqr")

        tele.feedback("powsqr", request.form)
        return redirect("/pdf/powsqr")
    else:
        return render_template("powsqr.html")


@app.route("/fraccions/", methods=["GET", "POST"])
def fraccions():
    if request.method == "POST":
        if app.debug:
            print("(Debug mode on...)")
            url = g.crea_fitxa(request.form)
        else:
            try:
                url = g.crea_fitxa(request.form)
            except Exception as exc:
                print(f"Error Fraccions ({exc})")
                tele.error("frac")
                return redirect("/latex_error/fraccions")
            tele.feedback("frac", request.form)
        return redirect(url)
    else:
        return render_template("fraccions.html")


@app.route("/ncient/", methods=["GET", "POST"])
def ncient():
    if request.method == "POST":
        try:
            g.ncient(request.form, solucions=False)
        except:
            print("Error Científica")
            tele.error("ncient")
            return redirect("/latex_error/ncient")
        tele.feedback("ncient", request.form)
        return redirect("/pdf/ncient")
    else:
        return render_template("ncient.html")


@app.route("/proporcionalitat/", methods=["GET", "POST"])
def proporcionalitat():
    if request.method == "POST":
        try:
            g.proporcionalitat(request.form, solucions=False)
        except:
            print("Error Proporcionalitat")
            tele.error("prop")
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
            print("Error Successions")
            tele.error("succ")
            return redirect("/latex_error/successions")
        tele.feedback("succ", request.form)
        return redirect("/pdf/successions")
    else:
        return render_template("successions.html")


@app.route("/polis/", methods=["GET", "POST"])
def polinomis():
    if request.method == "POST":
        if app.debug:
            print("(Debug mode on...)")
            url = g.crea_fitxa(request.form)
        else:
            try:
                url = g.crea_fitxa(request.form)
            except Exception as exc:
                print(f"Error Polinomis ({exc})")
                tele.error("polis")
                return redirect("/latex_error/polinomis")
            tele.feedback("polis", request.form)
        return redirect(url)
    else:
        return render_template("polinomis.html")


@app.route("/limits/", methods=["GET", "POST"])
def limits():
    if request.method == "POST":
        try:
            g.limits(request.form)
        except:
            print("Error Límits")
            tele.error("lim")
            return redirect("/latex_error/limits")
        tele.feedback("lim", request.form)
        return redirect("/pdf/limits")
    else:
        return render_template("limits.html")


@app.route("/derivades/", methods=["GET", "POST"])
def derivades():
    if request.method == "POST":
        try:
            g.derivades(request.form)
        except:
            print("Error Derivades")
            tele.error("dx")
            return redirect("/latex_error/derivades")
        tele.feedback("dx", request.form)
        return redirect("/pdf/derivades")
    else:
        return render_template("derivades.html")


# - - - - - - - - - - - - - - - - PLANES DD QUÍMICA - - - - - - - - - - - - - - - - - #


@app.route("/q/formul/", methods=["GET", "POST"])
def q_formul():
    if request.method == "POST":
        """g.q_formul(request.form)
        """
        try:
            g.q_formul(request.form)
        except:
            print("Error Formulació")
            tele.error("q_formul")
            return redirect("/latex_error/q_formul")
        tele.feedback("q_formul", request.form)
        return redirect("/pdf/q_formul")
    else:
        return render_template("q_formulac.html")


@app.route("/q/iso/", methods=["GET", "POST"])
def q_iso():
    if request.method == "POST":
        """g.q_iso(request.form)
        """
        try:
            g.q_iso(request.form)
        except:
            print("Error Isòtops")
            tele.error("q_iso")
            return redirect("/latex_error/q_iso")
        tele.feedback("q_iso", request.form)
        return redirect("/pdf/q_iso")
    else:
        return render_template("q_isotops.html")


# - - - - - - - - - - - - - - - - - - #


@app.route("/proves/", methods=["GET", "POST"])
def proves():
    if request.method == "POST":
        g.playground(request.form, solucions=False)
        return redirect("/pdf/successions")
    else:
        return render_template("provaforms.html")


@app.route("/provaforms/", methods=["GET", "POST"])
def provaforms():
    if request.method == "POST":
        form = request.form
        return render_template("provaforms.html", form=form, post=True)
    else:
        return render_template("provaforms.html")


@app.route('/pdf/<tema>')  # TODO això acabarà desapareixent amb el generador LaTeX únic (pq ja retorna la url)
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
    elif tema == "ncient":
        return redirect("/static/pdfs/ncient.pdf")
    elif tema == "proporcionalitat":
        return redirect("/static/pdfs/proporcionalitat.pdf")
    elif tema == "polinomis":
        return redirect("/static/pdfs/polinomis.pdf")
    elif tema == "successions":
        return redirect("/static/pdfs/successions.pdf")
    elif tema == "limits":
        return redirect("/static/pdfs/limits.pdf")
    elif tema == "derivades":
        return redirect("/static/pdfs/derivades.pdf")
    # química
    elif tema == "q_formul":
        return redirect("/static/pdfs/formulacio.pdf")
    elif tema == "q_iso":
        return redirect("/static/pdfs/isotops.pdf")
    else:
        return f"No s'ha trobat el pdf {tema}"


@app.route("/com/")
def com():
    return render_template("com.html")


@app.route("/donar/")
def donar():
    return render_template("donacions.html")


@app.route("/canvis/")
def canvis():
    return render_template("changelog.html")


@app.route("/contacte/")
def contacte():
    return render_template("contacte.html")


@app.route('/latex_error/<pdf>')
def latexerror(pdf):
    return (f"<h2>Hi ha hagut algun problema greu fent el teu pdf de {pdf}</h2>"
            f"<p><i>...o potser algú ha tingut l'error abans i ha quedat caigut, que també em passa.</i></p><hr>"
            f"<p>Si es manté avisa'm! (Twitter: @Rusca8 | Insta: @drusca8 | Mail: dynamicdeures@gmail.com)</p>")


@app.route('/<patillada>')
def notfound(patillada):
    return f"<h1>404</h1><br><h2>la pàgina {patillada} no existeix </h2>"


if __name__ == "__main__":  # això la fa córrer en local
    app.run(debug=True)
