
from flask import Flask,redirect,render_template, request, flash, url_for
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

# app.config['SQLALCHEMY_DATABASE_URI']='mysql://username:pass@localhost:port/databasename'

# the wrong version before installing the SQL Python connector
# app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/covid'

# After installing the SQL Python connector
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost:3307/covid'

db = SQLAlchemy(app)

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(user_id)


class User(UserMixin,db.Model):
  srfid=db.Column(db.String(20),primary_key=True)
  email=db.Column(db.String(100),unique=True)
  dob=db.Column(db.String(1000))
  def get_id(self):
    return (self.srfid) 



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



@app.route("/logout")
@login_required
def logout():
  logout_user()
  flash("You have been logged out successfully!", "success")
  return redirect(url_for('login'))


app.run(debug=True)
