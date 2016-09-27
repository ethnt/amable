from flask import Blueprint
from flask import render_template


base = Blueprint('base', __name__, template_folder='../templates/base')


@base.route('/')
def index():
    return "Hello world"


@base.route('/ui')
def ui():
    return render_template('ui.html')
