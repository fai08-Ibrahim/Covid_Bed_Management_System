
import json
from flask import Flask,redirect,render_template, request, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flask.globals import request, session
from flask_login import login_required,logout_user,login_user,login_manager,LoginManager,current_user
from flask_login import UserMixin
from sqlalchemy import create_engine, text
from werkzeug.security import generate_password_hash, check_password_hash 
import mysql.connector
from flask_mail import Mail


# mydatabase connection
local_server=True
app=Flask(__name__)
app.secret_key="fathyibrahim"

# To get the Unique User Access
login_manager=LoginManager(app)
login_manager.login_view='login'

# After installing the SQL Python connector
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost:3307/covid'

db = SQLAlchemy(app)

with open('config.json','r') as f:
  params=json.load(f)["params"]

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(user_id)


class User(UserMixin,db.Model):
  srfid=db.Column(db.String(20),primary_key=True)
  email=db.Column(db.String(100),unique=True)
  dob=db.Column(db.String(1000))
  def get_id(self):
    return (self.srfid) 
  

class Hospitaluser(UserMixin,db.Model):
  hid=db.Column(db.Integer,primary_key=True)
  hcode=db.Column(db.Integer,unique=True)
  email=db.Column(db.String(100))
  password=db.Column(db.String(1000))
  def get_id(self):
    return (self.hid) 


@app.route("/")
def home():
  return render_template("index.html")


@app.route('/signup', methods=['POST', 'GET'])
def signup():
  if request.method=="POST":
    srfid=request.form.get('srf')
    email=request.form.get('email')
    dob=request.form.get('dob')
    encpassword=generate_password_hash(dob)
    user=User.query.filter_by(srfid=srfid).first()
    user_email=User.query.filter_by(email=email).first()
    if user or user_email:
      flash("This SRF ID or Email is already in use.", "warning")
      return render_template("usersignup.html")

    with db.engine.connect() as conn:
      query = text(f"INSERT INTO `user` (`srfid`,`email`, `dob`) VALUES ('{srfid}','{email}','{encpassword}') ")
      new_user = conn.execute(query)
      conn.commit()

    flash("Accout Created Successfully!", "success")
    return render_template("index.html")

  return render_template("usersignup.html")



@app.route('/login', methods=['POST', 'GET'])
def login():
  if request.method=="POST":
    srfid=request.form.get('srf')
    dob=request.form.get('dob')
    user=User.query.filter_by(srfid=srfid).first()

    if user and check_password_hash(user.dob, dob):
      login_user(user)
      flash("Successful Login!", "info")
      return render_template("index.html")
    else:
      flash("Invalid Credentials!", "danger")
      return render_template("userlogin.html")

  return render_template("userlogin.html")


@app.route('/admin', methods=['POST', 'GET'])
def admin():
  if request.method=="POST":
    username=request.form.get('username')
    password=request.form.get('password')
    if(username==params['username'] and password==params['password']):
      session['user']=username
      flash("Login is successful","info")
      return render_template("addHosUser.html")
    else:
      flash("Invalid Credentials","danger")

  return render_template("admin.html")


@app.route("/logout")
@login_required
def logout():
  logout_user()
  flash("You have been logged out successfully!", "success")
  return redirect(url_for('login'))


@app.route("/addHospitalUser", methods=['POST','GET'])
def hospitalUser():
  if 'user' in session and session['user'] == params["username"]:
    if request.method == 'POST':
      hcode=request.form.get('hcode')
      email=request.form.get('email')
      password=request.form.get('password')
      encpassword=generate_password_hash(password)
      user_email=Hospitaluser.query.filter_by(email=email).first()
      if user_email:
        flash("This Email is already in use.", "warning")

      with db.engine.connect() as conn:
        query = text(f"INSERT INTO `hospitaluser` (`hcode`,`email`, `password`) VALUES ('{hcode}','{email}','{encpassword}') ")
        new_user = conn.execute(query)
        conn.commit()

      flash("DATA INSERTED", "success")

  else:
    flash("Please, log in and try again.", "warning")
    return redirect(url_for('admin'))


@app.route("/logoutadmin")
def logoutadmin():

  session.pop('user')
  flash("You have been logged out successfully!", "primary")

  return redirect(url_for('admin'))

if  __name__=='__main__':
  app.run(debug=True)
