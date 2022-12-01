from flask import Flask,render_template, url_for, request,redirect,flash,send_from_directory
#from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from flask_uploads import UploadSet, IMAGES, configure_uploads
#from flask_uploads import UploadSet, configure_uploads
from flask_wtf import FlaskForm
import requests

from flask_migrate import Migrate
import json
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired
from wtforms.validators import InputRequired,Length,ValidationError
# from email_validator import validate_email, EmailNotValidError
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename
from flask_wtf.file import FileField, FileAllowed, FileRequired

from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)
app._static_folder = ''
#UPLOAD_FOLDER = 'static/uploads/'
# UPLOAD_FOLDER='static/assets/uploads'
app.config['UPLOADED_PHOTOS_DEST'] = 'static/assets/uploads/'
#config to absolute path database.db 
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
app.config['SECRET_KEY']='josekevinhueso'




db=SQLAlchemy(app)
migrate=Migrate(app,db)
#  to hash passwords 
bcrypt=Bcrypt(app)

#allows app n flask login to wporkl togetehr 
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#load user 
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#database table 
# createes the values for which we will populate our db table->"User" with 
#creating objects creates rows 
class User(db.Model, UserMixin):
    #each id column which is a primary key; we will use to refrence the row with that id 
    id=db.Column(db.Integer, primary_key=True)
    #username must be unique; both username and password must be at most designated corresponding String length 
    username=db.Column(db.String(20), nullable=False,unique=True)
    password=db.Column(db.String(20), nullable=False)
    height=db.Column(db.String(20))
    major=db.Column(db.String(20))
    weight=db.Column(db.String(20))
    name=db.Column(db.String(20))
    gender=db.Column(db.String(20))
    bio=db.Column(db.String(450))


#linksk database to app    
with app.app_context():
    db.create_all()

#registration form; has username, password and submit fields; both username and pass take input, submit does not;
# submit field is a button 
# jinja tags are in html file to get the values
class RegisterForm(FlaskForm):
    #input req field, length parameters, in a way overriding above parameter; and render_kw simply displays vlue of corresponding key in text field 
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=7, max=20)], render_kw={"placeholder": "Password"})

    height = StringField(validators=[InputRequired(), Length(min=3, max=6)], render_kw={"placeholder": "Height"})
    major = StringField(validators=[InputRequired(), Length(min=1, max=20)], render_kw={"placeholder": "Major"})
    weight = StringField(validators=[InputRequired(), Length(min=1, max=6)], render_kw={"placeholder": "Weight"})

    name = StringField(validators=[InputRequired(), Length(min=2, max=10)], render_kw={"placeholder": "Name"})
    gender = StringField(validators=[InputRequired(), Length(min=1, max=8)], render_kw={"placeholder": "Gender"})
    bio = StringField(validators=[InputRequired(), Length(min=1, max=300)], render_kw={"placeholder": "Bio"})
    #register button
    submit = SubmitField('Register')

    



    #redundant as unique feature above requires it 
    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            raise ValidationError('That username already exists. Please choose a different one.')
        


# jinja tags are in html file to get the values; thus form.username etc
class LoginForm(FlaskForm):
    #same as aboce 
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=7, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField('Login')

#main page route 
@app.route("/")
def index():
    return render_template('index.html')




@app.route("/register",methods=['GET','POST'])
def register():
    # populuate with whatever user inputs 
    form=RegisterForm()
    
    # retunrs boolean;  it is used when a route can accept both GET and POST methods and you want to validate only on a POST request
    # if the post method is submited 
    
    if form.validate_on_submit():
        # from that reegister form; get the field password then get the data and ecrypt it 
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        # create object of user with encrypted password
        new_user = User(username=form.username.data, password=hashed_password, height=form.height.data, major=form.major.data, weight=form.weight.data, name=form.name.data, gender=form.gender.data,bio=form.bio.data )
        # go to table user within db and populate those columns 

        
        

        db.session.add(new_user)
        #save it 
        db.session.commit()
        #redirect to log in page after successfull creation 
        return redirect(url_for('login'))
    # existing_user_username = User.query.filter_by(username=form.username.data).first()
    # if existing_user_username:
    #     raise ValidationError('That username already exists Avner. Please choose a different one.')
    # else if the form returns false; meaning that post request wasnt succesfull, return to register page 
    return render_template("register.html", form=form)

global name
#login page route 
@app.route("/login", methods=['GET','POST'])
def login():
    # login form 
    form=LoginForm()
    # if the request to get is successfull 
    if form.validate_on_submit():
        #get the first occurence of that username entered 
        user = User.query.filter_by(username=form.username.data).first()
     
        #if user is in table 
        if user:
            #check is passwords match 
            if bcrypt.check_password_hash(user.password, form.password.data):
                #log that user in 
                login_user(user)
                #redirect them to profile page 
                posts=user
                return render_template("profile.html",posts=posts)
                #return redirect(url_for('profile'))

        
       
    # if user not in table the return them to login page         
    return render_template("login.html",form=form)


#profile page requires login 
@app.route('/profile', methods=['GET', 'POST','PUT'])
@login_required
#profile pagee
def profile():
    posts=User.query.all()
    return render_template('profile.html',posts=posts)


#logout which requires a log in to be applicable
@app.route('/logout', methods=['GET', 'POST'])
@login_required
#log the user out and redirect them to log in page 
def logout():
    logout_user()
    return redirect(url_for('login'))

    

class DeleteUserForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=7, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Delete')

@app.route('/delete2', methods=['GET','POST','DELETE','POST'])
def delete2():
   
    form = DeleteUserForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        #User.query.filter(User.id == user).delete()
        if user:
            #db.session.User.query.filter(user).delete()
            #db.session.query(User).filter(user).delete()
            db.session.delete(user)
            db.session.commit()
            flash('Your account has been successfully deleted. Hope to see you again.', 'success')
            return redirect(url_for('index'))

    return render_template('delete1.html', form=form)

def make_profile():
    # it generates new users with each run of the app 
    response = requests.get("https://randomuser.me/api/")
    #read API 
    #print(response.text)
    response= response.json() 
    #check the content type of the API 
    #print(response.headers.get("Content-Type"))

    gender=response['results'][0]['gender']
    fname=response['results'][0]['name']['first']
    lname=response['results'][0]['name']['last']

    location1= response['results'][0]['location']['country']
    location2= response['results'][0]['location']['state']

    age= response['results'][0]['dob']['age']
    pic= response['results'][0]['picture']['large']
    # return gender, fname, lname, location1, location2, age, pic 
    arr=[gender, fname, lname, location1, location2, age, pic]
    return arr

            
@app.route("/shellstack")
def shell_stack():
    trial=make_profile()
    return render_template("shell_stack.html", trial=trial)






#main 
if __name__=="__main__":
    app.run(debug=True)