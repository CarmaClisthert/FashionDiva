import os 
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
from werkzeug.utils import secure_filename
from db import get_db, get_wardrobe_class, get_wardrobe

# Image Processing
from ultralytics import YOLO
from rembg import remove
from PIL import Image

bp = Blueprint('wardrobe', __name__, url_prefix='/wardrobe')

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
saved_image = None

NORMALIZED_SIZE = (400, 400)

# AI model used for image classification
model = YOLO('fashion_detection.pt')

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/', methods=['GET', 'POST'])
def view_wardrobe():
    items = get_wardrobe()
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
        
            # Process image returns the class name of detection in photo
            filename = os.path.splitext(secure_filename(file.filename))[0] + ".png"
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(image_path)
            if request.form.get('item_type') == None:
                item_type = process_image(image_path)  # Run YOLO on saved image
            else:
                item_type = request.form.get('item_type') 

            remove_background(image_path)
            
            resize_image(image_path, item_type)

            db = get_db()
            db.execute(
                'INSERT INTO clothing_items (user_id, image_path, item_type) VALUES(?, ?, ?)',
                (session['user_id'], filename, item_type),
            )
            db.commit()
            return redirect(url_for('wardrobe.view_wardrobe'))
    return render_template("upload_closet.html")

def process_image(img_path):
    results = model.predict(img_path, conf=.6)
    for result in results:
        boxes = result.boxes
        for box in boxes:
            class_id = int(box.cls[0])
            class_name = model.names[class_id]
            
            # Since there are more classes than we have sections - check and test as one
            if class_name in ['Tshirt', 'Dress', 'shirt', 'sweater']:
                class_name = 'tops'
            elif class_name in ['pants', 'short', 'skirt']:
                class_name = 'pants'
            elif class_name == 'shoes':
                return 'shoes'
            print(class_name)
            return class_name
        
def remove_background(image_path):
    with Image.open(image_path) as img:
        img = img.convert("RGBA")
        result = remove(img)
        result.save(image_path, format="PNG") 

def resize_image(image_path, item_type):
    with Image.open(image_path) as img:
        img = img.convert("RGBA")  # Ensure transparency
        img = img.resize(NORMALIZED_SIZE, Image.Resampling.LANCZOS)
        img.save(image_path)


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

    return redirect(url_for('wardrobe.view_wardrobe'))

@bp.route('/debug')
def debug_db():
    db = get_db()
    items = db.execute('SELECT * FROM clothing_items').fetchall()
    for item in items:
        print(dict(item))  # convert Row object to dictionary
    return "Check console for output"