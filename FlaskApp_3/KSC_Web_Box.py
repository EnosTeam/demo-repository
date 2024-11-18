from flask import  render_template, Blueprint

Box = Blueprint('Box', __name__)

@Box.route('/gallery')
def gallery():
    return render_template('gallery.html')
