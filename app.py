# app.py
# Created by W. Mariam Sanou on 4/7/25.
# cd fashiondiva --> source .venv/bin/activate --> flask --app app init-db

from flask import Flask, render_template, request, redirect, url_for, flash
from database.db import get_user, add_user
from database import db

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'fashiondiva'
    app.config['DATABASE'] = 'instance/fashiondiva.sqlite'

    db.init_app(app)

    @app.route("/")
    def home():
        return render_template("index.html")

    @app.route("/login", methods=['POST'])
    def login():
        username = request.form.get('username')
        password = request.form.get('password')

        user = get_user(username)
        if user and user['password'] == password:
            return redirect(url_for('main'))
        else:
            flash('Invalid username or password', 'error')
            return redirect(url_for('signup'))

    @app.route("/signup", methods=['GET', 'POST'])
    def signup():
        if request.method == 'POST':
            name = request.form.get('signup-name')
            password = request.form.get('signup-password')
            confirm_password = request.form.get('confirm-password')

            existing_user = get_user(name)

            if existing_user:
                flash('Username already exists', 'error')
            elif password != confirm_password:
                flash('Passwords do not match', 'error')
            else:
                add_user(name, password)
                return redirect(url_for('wardrobe.upload'))

        return render_template("signin.html")
        
        # blueprint to upload clothing items and to view them
    import wardrobe
    app.register_blueprint(wardrobe.bp)
    
    @app.route("/tops")
    def tops():
        return render_template("tops.html")
        
    @app.route("/pants")
    def pants():
        return render_template("pants.html")
        
    @app.route("/accessories")
    def accessories():
        return render_template("accessories.html")
        
    @app.route("/shoes")
    def shoes():
        return render_template("shoes.html")
    
    @app.route("/uploadcloset")
    def upload_closet():
        return render_template("upload_closet.html")
        
    @app.route("/closetsaved")
    def closetsaved():
        return render_template("saved_closet.html")
        
  


        
    @app.route("/main")
    def main():
        return render_template("mainpage.html")

    return app
