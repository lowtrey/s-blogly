# Models for Blogly

from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
  db.app = app
  db.init_app(app)

# Models 
class User(db.Model):
  __tablename__ = "users"

  id = db.Column(db.Integer,
                  primary_key=True,
                  autoincrement=True)

  first_name = db.Column(db.String(50),
                    nullable=False)

  last_name = db.Column(db.String(50),
                    nullable=False)

  image_url = db.Column(db.String(1000), 
                    nullable=False, 
                    default="https://i.stack.imgur.com/l60Hf.png")

  def __repr__(self):
    return f"<User full_name={self.full_name}>"

  @property
  def full_name(self):
    return f"{self.first_name} {self.last_name}"


class Post(db.Model):

  __tablename__ = "posts"

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)

  title = db.Column(db.Text, nullable=False, unique=True)

  content = db.Column(db.Text, nullable=False)

  created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

  user_id = db.Column(db.Integer, db.ForeignKey("users.id"))