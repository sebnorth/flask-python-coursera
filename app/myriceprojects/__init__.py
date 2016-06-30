
from flask import Blueprint

myriceprojects = Blueprint('myriceprojects', __name__)

from . import routes
