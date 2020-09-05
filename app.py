from flask import Flask, request, render_template, redirect, url_for
from flask_debugtoolbar import DebugToolbarExtension
from forex_python.converter import CurrencyRates, CurrencyCodes, Decimal
import math

app = Flask(__name__)
app.config['SECRET_KEY'] = "327-446-427"
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
c = CurrencyRates(force_decimal=True)
cc = CurrencyCodes()


def get_rate(con_from, con_to, amount):
    '''Handles the rate conversion to 2 decimals and gets currency symbol.'''
    try:
        rate = (cc.convert(con_from, con_to, amount))
        return rate
    except:
        return False


@app.route("/")
def home_page():
    """home page"""
    return render_template("index.html")


@app.route("/convert")
def convert():
    """gets input, converts via forex converter methods, renders response template or redirect to error"""

    try:
        con_from = request.args["convert_from"]
        con_to = request.args["convert_to"]
        amount = Decimal(request.args["amount"])

        converted_amt = c.convert(con_from, con_to, amount)
        display_amt = round(converted_amt, 2)

        return render_template("rate.html", display_amt=display_amt, con_from=con_from, con_to=con_to)
    except:
        return redirect(url_for('error'))


@app.route("/error")
def error():
    """display error message"""

    return render_template("error.html")
