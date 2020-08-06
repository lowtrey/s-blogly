from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag
from datetime import datetime

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


# User Routes
@app.route("/")
def redirect_to_users():
  """"""
  return redirect("/users")


@app.route("/users")
def show_users():
  """Show Full List of Users"""
  # Sort Users by last_name, first_name
  users = User.query.filter().order_by(User.last_name, User.first_name)
  return render_template("users.html", users=users)


@app.route("/users/new")
def show_add_form():
  """Show Add User Form"""
  return render_template("add_user_form.html")


@app.route("/users/new", methods=["POST"])
def add_user():
  """Process New User Data | Redirect to Users List"""
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


@app.route("/users/<int:user_id>")
def show_user(user_id):
  """Show User Details"""
  user = User.query.get_or_404(user_id)
  return render_template("user_details.html", user=user)


@app.route("/users/<int:user_id>/edit")
def show_edit_form(user_id):
  """Show Edit User Form"""
  user = User.query.get_or_404(user_id)
  return render_template("edit_user_form.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def edit_user(user_id):
  """Edit User | Redirect to Users List"""
  user = User.query.get_or_404(user_id)

  # Collect Form Data
  user.first_name = request.form["first"]
  user.last_name = request.form["last"]
  user.image_url = request.form["url"]

  # Update User | Redirect
  db.session.add(user)
  db.session.commit()

  return redirect("/users")


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
  """Delete User | Redirect to Users List"""
  user = User.query.get_or_404(user_id)
  db.session.delete(user)
  db.session.commit()

  return redirect("/users")


@app.route("/users/<int:user_id>/posts/new")
def show_add_post_form(user_id):
  """Show Add Post Form"""
  user = User.query.get_or_404(user_id)
  print(user)
  return render_template("add_post_form.html", user=user)


@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def add_post(user_id):
  """Add Post | Redirect to User Details"""
  title = request.form["title"]
  content = request.form["content"]
  post = Post(title=title, content=content, user_id=user_id)

  db.session.add(post)
  db.session.commit()

  return redirect(f"/users/{user_id}")


# Post Routes
@app.route("/posts/<int:post_id>")
def show_post(post_id):
  """Show Post Details"""
  post = Post.query.get_or_404(post_id)
  return render_template("post.html", post=post)


@app.route("/posts/<int:post_id>/edit")
def show_edit_post_form(post_id):
  post = Post.query.get_or_404(post_id)
  return render_template("edit_post_form.html", post=post)


@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def edit_post(post_id):
  """Edit Post | Redirect to Post Details"""
  post = Post.query.get_or_404(post_id)

  # Collect Form Data
  post.title = request.form["title"]
  post.content = request.form["content"]

  # Update Post | Redirect
  db.session.add(post)
  db.session.commit()

  return redirect(f"/posts/{post_id}")


@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
  """Delete Post | Redirect to User Details"""
  user_id = Post.query.get_or_404(post_id).user_id
  
  Post.query.filter(Post.id == post_id).delete()
  db.session.commit()

  return redirect(f"/users/{user_id}")

  # TODO: Update timestamp when post is edited
  # TODO: Show updated_at instead of created_at 


# Tag Routes
@app.route("/tags")
def list_tags():
  """List Tags | Link to Tag Details"""
  tags = Tag.query.all()
  return render_template("tags.html", tags=tags)