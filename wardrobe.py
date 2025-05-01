import os 
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
from werkzeug.utils import secure_filename
from db import get_db

bp = Blueprint('wardrobe', __name__, url_prefix='/wardrobe')

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/', methods=['GET', 'POST'])
def view_wardrobe():
    db = get_db()
    items = db.execute('SELECT * FROM clothing_items WHERE user_id = ?', (session['user_id'],)).fetchall()
    return render_template('upload_closet.html', items=items)

@bp.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
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
            return redirect(url_for('wardrobe.view_wardrobe'))
    return render_template("upload_closet.html")

@bp.route('/delete/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    db = get_db()
    item = db.execute('SELECT * FROM clothing_items WHERE id = ? AND user_id = ?', 
                      (item_id, session['user_id'])).fetchone()
    
    if item is None:
        return redirect(url_for('wardrbe.view_wardrobe'))
    
    image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], item['image_path'])
    if os.path.exists(image_path):
        os.remove(image_path)
    
    db.execute('DELETE FROM clothing_items WHERE id = ?', (item_id,))
    db.commit()
    flash('Item deleted successfully!')

    return redirect(url_for('wardrobe.view_wardrobe'))

@bp.route('/debug')
def debug_db():
    db = get_db()
    items = db.execute('SELECT * FROM clothing_items').fetchall()
    for item in items:
        print(dict(item))  # convert Row object to dictionary
    return "Check console for output"