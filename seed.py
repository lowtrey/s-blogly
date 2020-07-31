# Seed file to make sample data for users db.

from models import db, User, Post
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it.
User.query.delete()

# Add users
quinton = User(first_name="Quinton", last_name="Price", image_url="https://avatars2.githubusercontent.com/u/31049090?s=460&u=11cf5bf4d42580daef1e0b2fa0755f7865d8362c&v=4")
chaya = User(first_name="Chaya", last_name="Deaver", image_url="https://avatars2.githubusercontent.com/u/52929582?s=460&u=48e440d7ccfffdcb8b297f704cb081a68b85e240&v=4")
desmend = User(first_name="Desmend", last_name="Jetton", image_url="https://avatars2.githubusercontent.com/u/28575803?s=460&u=70b7f2f697d2a828b28c05e3e485abbfad7b0462&v=4")
chris = User(first_name="Chris", last_name="Warren", image_url="https://avatars2.githubusercontent.com/u/40346297?s=460&u=6b503dae4adda68c130d977ee85e103fe9ebbe55&v=4")
haja = User(first_name="Haja", last_name="Childs", image_url="https://avatars3.githubusercontent.com/u/57027705?s=460&u=3198d350eaa81e16b2ac856a824422de54513429&v=4")
ojo = User(first_name="Ojo", last_name="Mayowa", image_url="https://avatars3.githubusercontent.com/u/48096465?s=460&u=5ba31c59e36f478fb42f1058c2b417e4312fc392&v=4")

# Add new objects to session, so they'll persist.
db.session.add(quinton)
db.session.add(chaya)
db.session.add(desmend)
db.session.add(chris)
db.session.add(haja)
db.session.add(ojo)

# Commit - otherwise, this never gets saved!
db.session.commit()