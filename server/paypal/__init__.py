from flask import Blueprint

paypal = Blueprint("paypal", __name__)

from . import views
