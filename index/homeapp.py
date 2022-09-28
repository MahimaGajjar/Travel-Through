from flask import Blueprint, render_template

bp = Blueprint('homeapp', __name__)

@bp.route('/', methods =['GET', 'POST'])
def index():
    return render_template('index.html')