import os
#name of the directory where the project resides
basedir = os.path.abspath(os.path.dirname(__file__))
class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "random-password-that-you-will-never-guess"
    
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or f"sqlite:///{os.path.join(basedir,'app.db')}"
  
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_DIRECTORY = "uploads"