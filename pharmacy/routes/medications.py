from flask import Blueprint, render_template
from flask_login import login_required

medications_bp = Blueprint('medications', __name__)

@medications_bp.route('/medications')
@login_required
def index():
    return render_template('medications/index.html')