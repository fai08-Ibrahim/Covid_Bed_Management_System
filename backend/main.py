
from flask import Flask,redirect,render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask.globals import request, session
from flask_login import login_required,logout_user,login_user,login_manager,LoginManager,current_user
from flask_login import UserMixin
from sqlalchemy import create_engine, text
from werkzeug.security import generate_password_hash, check_password_hash 
import mysql.connector


# mydatabase connection
local_server=True
app=Flask(__name__)
app.secret_key="fathyibrahim"

# To get the Unique User Access
login_manager=LoginManager(app)
login_manager.login_view='login'

# app.config['SQLALCHEMY_DATABASE_URI']='mysql://username:password@localhost/databasename'

# the wrong version before installing the SQL Python connector
# app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/covid'

# After installing the SQL Python connector
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost:3307/covid'

db = SQLAlchemy(app)

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))


# class Test(db.Model):
#   id=db.Column(db.Integer,primary_key=True)
#   name=db.Column(db.String(50))


class User(db.Model):
  srfid=db.Column(db.String(20),primary_key=True)
  email=db.Column(db.String(20),unique=True)
  dob=db.Column(db.String(20))



@app.route("/")
def home():
  return render_template("index.html")

@app.route("/usersignup")
def usersignup():
  return render_template("usersignup.html")

@app.route('/signup', methods=['POST', 'GET'])
def signup():
  if request.method=="POST":
    srfid=request.form.get('srf')
    email=request.form.get('email')
    dob=request.form.get('dob')
    # print(srfid,email,dob)
    encpassword=generate_password_hash(dob)

    #  new_user=db.engine.execute(f"INSERT INTO `user` (`srfid`,`email`,`dob`) VALUES ('{srfid}','{email}','{encpassword}') ")
    with db.engine.connect() as conn:
      query = text(f"INSERT INTO `user` (`srfid`,`email`, `dob`) VALUES ('{srfid}','{email}','{encpassword}') ")
      new_user = conn.execute(query)
      conn.commit()

    return 'USER ADDED'

  return render_template("usersignup.html")


@app.route("/userlogin")
def userlogin():
  return render_template("userlogin.html")


# Testing for the db connection
# @app.route("/test")
# def test():
#   try:
#     a=Test.query.all()
#     print(a)
#     return "DATABASE IS CONNECTED"
#   except Exception as e:
#     print(e)
#     return f"DATABASE IS NOT CONNECTED {e}"

app.run(debug=True)
