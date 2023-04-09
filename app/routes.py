from flask import render_template,url_for,redirect,flash,request,abort,current_app
from werkzeug.utils import secure_filename
from werkzeug.urls import url_parse
from flask_login import current_user,login_user,logout_user,login_required
import os
from mimetypes import guess_extension

from app import app,db
from app.models import User
from app.forms import LoginForm,RegisterForm




#AUTHENTICATION ROUTES---------------------------------------------------------------------------------------------------------------


#login
@app.route('/login',methods=['POST','GET'])
def login():
    #page title 
    title = 'Login'

    form = LoginForm()
    if current_user.is_authenticated: # type: ignore
        return redirect(url_for('index'))

    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data ).first()
        
        #check user credentials
        if user is None or not user.check_password(form.password.data):
            flash('User is invalid or credentials are not correct',"alert alert-danger")
            return redirect(url_for('login'))
        
        login_user(user,remember=form.remember_me.data)
        
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)  
    
    return render_template('login.html',title = title , form = form )

#logout
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

#register 
@app.route('/register',methods=['POST','GET'])
def register():
    title = "register"
    if current_user.is_authenticated: # type: ignore
        return redirect(url_for('index'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username = form.username.data ,email = form.email.data) # type: ignore
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        
        return redirect(url_for('login'))
    
    
    return render_template('register.html',form = form,title = title)

#-----------------------------------------------------------------------------------------------------------------------------

#Audio upload and handling routes


#main views 
@app.route('/')
@login_required
def index():
    title = "Home"
    return render_template('index.html', title=title)

@app.route('/audio-upload', methods=['POST'])
def audio_upload():
    #check if audio  file was uploaded
    if 'audio_file' in request.files:
        file = request.files['audio_file']
        extname = guess_extension(file.mimetype)
        if not extname:
            abort(400)

        current_user_id = request.form.get("current_user")
        
        dir_path = os.path.join(current_app.instance_path,current_app.config.get("UPLOAD_DIRECTORY"),secure_filename(current_user_id)) 
        print(dir_path)
        print(os.path.exists(dir_path))
        if not os.path.exists(dir_path):
           os.mkdir(dir_path)
        file.save(os.path.join(dir_path,f"first_audio{extname}"))

    return "audio_uploaded_with_sucess"
   