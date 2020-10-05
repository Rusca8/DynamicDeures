from urllib.parse import quote_plus as quote


def urlfor(latex, t=0):
    url = "https://www.wolframalpha.com/input/?i="
    if t == "dx":
        latex = "derivative of " + latex
    url += quote(latex)
    return url
