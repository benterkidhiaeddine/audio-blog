import os
#name of the directory where the project resides
basedir = os.path.abspath(os.path.dirname(__file__))
class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "random-password-that-you-will-never-guess"
    
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or f"sqlite:///{os.path.join(basedir,'app.db')}"
  
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_DIRECTORY = "uploads"

    #configuration for flask mail

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "thekizzer.swag@gmail.com"
    
    MAIL_PASSWORD = "btyijoboychpmkng"