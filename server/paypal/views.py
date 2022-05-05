from sre_constants import SUCCESS

from flask import render_template
from . import paypal

@paypal.route('/')
def index():
    return render_template("paypal/index.html")