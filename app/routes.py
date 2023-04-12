from flask import render_template,url_for,redirect,flash,request,abort,current_app,send_from_directory
from werkzeug.utils import secure_filename
from werkzeug.urls import url_parse
from flask_login import current_user,login_user,logout_user,login_required
import os
from mimetypes import guess_extension

from app import app,db
from app.models import User
from app.forms import LoginForm,RegisterForm,PasswordResetForm,RequestResetForm,SearchForm
from app.mail import send_email



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
    title = "Register"
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

#password reset functionality --------------------------------------------------------------------------------------------------------------------
#request reset 
@app.route("/request_reset",methods = ["POST","GET"])
def request_reset():


    form = RequestResetForm()
    title = "Request Reset"

    if form.validate_on_submit():
        user =User.query.filter_by(email = form.email.data).first()
        if not user:
            flash("A user with  this email doesn't exist","alert alert-warning")
        else:
            send_email(user)
            flash("check your Email","alert alert-success")
    
    return render_template("request_reset.html",form = form , title = title)


#reset password 
@app.route("/reset_password/<token>",methods=['GET','POST'])
def reset_password(token):
    user = User.verify_reset_token(token)

    if user is None:
        flash("token is invlaid or has expired","alert alert-warning")
        return redirect(url_for('request_reset'))

    form = PasswordResetForm()
    title = "Reset Password"
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash("password has been reset successfully","alert alert-success")
        return redirect(url_for('login'))
    
    return render_template("reset_password.html",title=title,form = form ,token = token)


#-----------------------------------------------------------------------------------------------------------------------------

#Audio upload and handling routes


#main views 
@app.route('/')
@login_required
def index():

    question_list=[
        "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Cumque, neque? Quia, veritatis?",
        "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Cumque, neque? Quia, veritatis?",
        "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Cumque, neque? Quia, veritatis?",
        "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Cumque, neque? Quia, veritatis?",
        "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Cumque, neque? Quia, veritatis?",
        "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Cumque, neque? Quia, veritatis?",
        "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Cumque, neque? Quia, veritatis?",
        "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Cumque, neque? Quia, veritatis?",
        "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Cumque, neque? Quia, veritatis?",
        "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Cumque, neque? Quia, veritatis?",
      
    ]
    title = "Home"
    return render_template('index.html', title=title, question_list = question_list)

@app.route('/audio-upload', methods=['POST'])
@login_required
def audio_upload():
    #check if audio  file was uploaded
    if 'audio_file' in request.files:
        file = request.files['audio_file']
        extname = guess_extension(file.mimetype)
        #eventualy write code for validating extention types
        print(extname)
        if not extname:
            abort(400)

        question_number = request.form.get("question_number")
        dir_path = os.path.join(current_app.instance_path,current_app.config.get("UPLOAD_DIRECTORY"),current_user.get_id()) 
        print(dir_path)
        print(os.path.exists(dir_path))
        if not os.path.exists(dir_path):
           os.mkdir(dir_path)
        file.save(os.path.join(dir_path,f"{question_number}{extname}"))

    return "audio_uploaded_with_success"


@app.route("/<int:user_id>/audios")
@login_required
def user_audios(user_id):
    file_paths = os.listdir(os.path.join(current_app.instance_path,current_app.config['UPLOAD_DIRECTORY'],str(user_id)))
    file_names = [ os.path.splitext(file)[0] for file in file_paths]
    files = []
    for file_path,file_name in zip(file_paths,file_names):
        files.append({"name":file_name,"path":file_path})

    title = "Audio answers"
    return render_template("user_audios.html",files = files,title = title ,user_id = user_id)
   


@app.route('/uploads/<int:user_id>/<path:filename>')
@login_required
def download_file(user_id,filename):
    
    return send_from_directory(os.path.join(current_app.instance_path,current_app.config['UPLOAD_DIRECTORY'],str(user_id)),
                               filename)



#Search users form 
@app.route("/search",methods=['POST','GET'])
@login_required
def search():

    form = SearchForm()
    title = "Search User"

    if form.validate_on_submit():
        searched_user = form.searched.data
        search_result = User.query.filter_by( username = searched_user).first()
        print(search_result)
        if search_result is None:
            flash("the searched user was not found","alert alert-warning")
            return redirect(url_for('search'))    

        return redirect(url_for('user_audios',user_id = search_result.id))
        
        


    return render_template("listen.html",form = form , title = title)