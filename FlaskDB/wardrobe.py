import os

from flask import(
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)
from werkzeug.utils import secure_filename

from FlaskDB.db import get_db
from FlaskDB.auth import load_logged_in_user

bp = Blueprint('wardrobe', __name__, url_prefix='/wardrobe')

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':

        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected ffile')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

            db = get_db()
            db.execute(
                'INSERT INTO clothing_items (user_id, image_path) VALUES(?, ?)',
                (session['user_id'], filename),
            )
            db.commit()
            return redirect(url_for('wardrobe.debug_db'))
            #return redirect(url_for('wardrobe.upload_file', name=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@bp.route('/debug')
def debug_db():
    db = get_db()
    items = db.execute('SELECT * FROM clothing_items').fetchall()
    for item in items:
        print(dict(item))  # convert Row object to dictionary
    return "Check console for output"