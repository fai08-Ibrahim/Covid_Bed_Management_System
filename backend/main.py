
from flask import Flask,redirect,render_template
from flask_sqlalchemy import SQLAlchemy
import mysql.connector

# mydatabase connection
local_server=True
app=Flask(__name__)
app.secret_key="fathyibrahim"

# app.config['SQLALCHEMY_DATABASE_URI']='mysql://username:password@localhost/databasename'

# the wrong version before installing the SQL Python connector
# app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/covid'

# After installing the SQL Python connector
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/covid'

db = SQLAlchemy(app)

class Test(db.Model):
  id=db.Column(db.Integer,primary_key=True)
  name=db.Column(db.String(50))

@app.route("/")
def home():
  return render_template("index.html")

# Testing for the db connection
@app.route("/test")
def test():
  try:
    a=Test.query.all()
    print(a)
    return "DATABASE IS CONNECTED"
  except Exception as e:
    print(e)
    return f"DATABASE IS NOT CONNECTED {e}"

app.run(debug=True)
