from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)

# Configure and Initialize Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

# Configure Debug Toolbar
app.config['SECRET_KEY'] = "chickens"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)


@app.route("/")
def redirect_to_users():
  """"""
  return redirect("/users")


@app.route("/users")
def show_users():
  """Show Full List of Users"""
  users = User.query.all()
  return render_template("users.html", users=users)


@app.route("/users/new")
def show_add_form():
  """Show Form for Adding Users"""
  return render_template("add_user_form.html")


@app.route("/users/new", methods=["POST"])
def add_user():
  """Process New User Data | Redirect to Full List"""
  # Collect Form Data
  first = request.form["first"]
  last = request.form["last"]
  url = request.form["url"]
  url = url if url else None

  # Create User | Add to DB | Redirect
  new_user = User(first_name=first, last_name=last, image_url=url)
  db.session.add(new_user)
  db.session.commit()

  return redirect("/users")