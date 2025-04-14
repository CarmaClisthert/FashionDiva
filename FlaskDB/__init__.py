# This file initializes all of the blueprints for the different sections of the web app.
# To run int terminal for the virtual environment .venv/Scripts/activate 
# Then type:  flask --app FlaskDB run --debug
# If the database needs to be reinitialized type: flask --app FlaskDB init-db

# The current routing goes from the signin page until you register and login then takes you to a wardrobe page I am working on to upload photos into the server.
import os 

from flask import Flask

UPLOAD_FOLDER = 'FlaskDB/wardrobe_uploads'

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'FlaskDB.sqlite'),
        UPLOAD_FOLDER = UPLOAD_FOLDER,
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in 
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    from . import db
    db.init_app(app)
    
    from . import auth
    app.register_blueprint(auth.bp)

    from . import wardrobe
    app.register_blueprint(wardrobe.bp)

    return app