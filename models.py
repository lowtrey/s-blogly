# Models for Blogly

from flask_sqlalchemy import SQLAlchemy 

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