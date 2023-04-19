from flask import Blueprint

bp = Blueprint('recruit', __name__)

from app.recruit import main