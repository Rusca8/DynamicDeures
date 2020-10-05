from urllib.parse import quote_plus as quote


def urlfor(latex, t=0):
    url = "https://www.wolframalpha.com/input/?i="
    latex = latex.replace(r"\,", "").replace(r"\frac{1}{2}", "{1/2}")
    if t == "dx":
        latex = "derivative of " + latex
    url += quote(latex)
    return url
