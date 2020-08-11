from flask import Flask, request, render_template, redirect, flash, session
from models import db, connect_db, User, Post, Tag, PostTag
from flask_debugtoolbar import DebugToolbarExtension
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
def show_feed():
  """Show Post Feed"""
  posts = Post.query.filter().order_by(Post.created_at.desc())
  return render_template("feed.html", posts=posts)


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
  return render_template("user.html", user=user)


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

# Post Routes
@app.route("/users/<int:user_id>/posts/new")
def show_add_post_form(user_id):
  """Show Add Post Form"""
  user = User.query.get_or_404(user_id)
  tags = Tag.query.all()
  return render_template("add_post_form.html", user=user, tags=tags)


@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def add_post(user_id):
  """Add Post | Redirect to User Details"""
  # Gather Form Data
  title = request.form["title"]
  content = request.form["content"]
  tag_ids = request.form.getlist("tags")
  post = Post(title=title, content=content, user_id=user_id)
  # Add Tags to Post
  if tag_ids:
    for tag_id in tag_ids:
      tag = Tag.query.get_or_404(int(tag_id))
      post.tags.append(tag)
  # Commit Post & Redirect
  db.session.add(post)
  db.session.commit()
  return redirect(f"/users/{user_id}")


@app.route("/posts/<int:post_id>")
def show_post(post_id):
  """Show Post Details"""
  post = Post.query.get_or_404(post_id)
  return render_template("post.html", post=post)


@app.route("/posts/<int:post_id>/edit")
def show_edit_post_form(post_id):
  """Show Edit Post Form"""
  post = Post.query.get_or_404(post_id)
  tags = Tag.query.all()
  return render_template("edit_post_form.html", post=post, tags=tags)


@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def edit_post(post_id):
  """Edit Post | Redirect to Post Details"""
  post = Post.query.get_or_404(post_id)
  # Collect Form Data
  post.title = request.form["title"]
  post.content = request.form["content"]
  post.tags = []
  tag_ids = request.form.getlist("tags")
  # Update Tags
  if tag_ids:
    for tag_id in tag_ids:
      tag = Tag.query.get_or_404(int(tag_id))
      post.tags.append(tag)
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


@app.route("/tags/<int:tag_id>")
def show_tag(tag_id):
  """Show Tag Details"""
  tag = Tag.query.get_or_404(tag_id)
  return render_template("tag.html", tag=tag)


@app.route("/tags/new")
def show_add_tag_form():
  """Show Add Tag Form"""
  return render_template("add_tag_form.html")


@app.route("/tags/new", methods=["POST"])
def add_tag():
  """Add Tag | Redirect to Tags List"""
  tag_name = request.form["tag"]
  new_tag = Tag(name=tag_name)
  db.session.add(new_tag)
  db.session.commit()
  return redirect("/tags")


@app.route("/tags/<int:tag_id>/edit")
def show_edit_tag_form(tag_id):
  """Show Edit Tag Form"""
  tag = Tag.query.get_or_404(tag_id)
  return render_template("edit_tag_form.html", tag=tag)


@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def edit_tag(tag_id):
  """Edit Tag | Redirect to Tags List"""
  tag = Tag.query.get_or_404(tag_id)
  tag.name = request.form["tag"]
  db.session.add(tag)
  db.session.commit()
  return redirect("/tags")


@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
  """Delete Tag | Redirect to Tags List"""
  tag = Tag.query.get_or_404(tag_id)
  db.session.delete(tag)
  db.session.commit()
  return redirect("/tags")