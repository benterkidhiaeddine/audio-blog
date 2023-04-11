import jwt
import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from app import db,login
from flask import current_app

class User(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),unique=True)
    email = db.Column(db.String(120),unique=True)
    hashed_password = db.Column(db.String(128))
    audios = db.relationship('Audio',backref='author')

    def __repr__(self):
        return f"<User {self.username}>"

    def set_password(self,password):
        self.hashed_password = generate_password_hash(password)
        

    def check_password(self,password):
        return check_password_hash(self.hashed_password,password)
    
    def generate_reset_token(self,expiration = 300):
        reset_token = jwt.encode(
            {
                "user_id": self.id,
                "exp": datetime.datetime.now(tz=datetime.timezone.utc)
                       + datetime.timedelta(seconds=expiration)
            },
            current_app.config['SECRET_KEY'],
            algorithm="HS256"
        )
        return reset_token
    #if the token is correct return the user object if not return none
    @staticmethod
    def verify_reset_token(token):
        try:
            user_id = jwt.decode(
                token,
                current_app.config["SECRET_KEY"],
                leeway=datetime.timedelta(seconds=10),
                algorithms=["HS256"]
            )["user_id"]
            
        except Exception as e:
            print(e)
            return None
       
        return User.query.get(user_id)



class Audio(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    answer_number = db.Column(db.Integer)
    audio_URL = db.Column(db.String(120))
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))

@login.user_loader
def load_user(id):
    return User.query.get(int(id))