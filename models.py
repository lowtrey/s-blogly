"""Models for Blogly."""

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

  image_url = db.Column(db.String(500), 
                    nullable=False, 
                    default="https://i.stack.imgur.com/l60Hf.png")
  
  # @classmethod
  # def get_by_species(cls, species):
  #   return cls.query.filter_by(species = species).all()

  # @classmethod
  # def get_all_hungry(cls):
  #   return cls.query.filter(Pet.hunger > 20).all()

  # def __repr__(self):
  #   p = self
  #   return f"<Pet id={p.id} name={p.name} species={p.species} hunger={p.hunger} "

  # def greet(self):
  #   return f"Hi, I'm {self.name} the {self.species}."

  # def feed(self, amt = 20):
  #   """Update hunger based off of amt"""
  #   self.hunger -= amt
  #   self.hunger = max(self.hunger, 0)
