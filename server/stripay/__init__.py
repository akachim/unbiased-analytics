from flask import Blueprint

stripay = Blueprint("stripay", __name__)

from . import views