import os 
from flask import Blueprint, request, redirect, session, url_for, render_template
from werkzeug.utils import secure_filename
from database.db import get_db

bp = Blueprint('wardrobe', __name__)

@bp.route('/upload', methods=['POST'])
def upload():
    image = request.file.get('image')
    if not image:
        return redirect(url_for('wardrobe.view_wardrobe'))
    
    filename = secure_filename(image.filename)
    upload_path = os.path.join('app', 'static', 'uploads', filename)
    image.save(upload_path)

    # add mmfashion attribute and landmark recognition here

    db = get_db()
    db.execute('INSERT INTO clothing_items (user_id, filename VALUES (?, ?,)',
               (session['user_id'], filename))
    db.commit()

    return redirect(url_for('wardrobe.view_wardrobe'))

@bp.route('/wardrobe')
def veiw_wardrobe():
    db = get_db()
    items = db.execute('SELECT * FROM clothing_items WHERE user_id = ?', (session['user_id'],)).fetchall()
    return render_template('upload_closet.html', items=items)
