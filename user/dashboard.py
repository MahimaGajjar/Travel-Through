from flask import Blueprint, render_template

bp_dashboard = Blueprint('dashboard', __name__)

@bp_dashboard.route('/dashboard')
def dashboard():
    return render_template('user/dashboard.html')