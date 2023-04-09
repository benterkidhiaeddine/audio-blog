from flask import Flask
from config import Config
from flask_sqlalchemy  import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os


app = Flask(__name__)

app.config.from_object(Config)


try:
    os.makedirs(os.path.join(
        app.instance_path,
        app.config.get('UPLOAD_DIRECTORY', 'uploads')
    ), exist_ok=True)
except:
    pass



db = SQLAlchemy(app)

migrate = Migrate(app,db) 

login = LoginManager(app)

login.login_view = 'login'

#import routes for different views , and models for the database models
from . import routes,models