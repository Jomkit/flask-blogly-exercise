from models import User, Post, db 
from app import app

# create all tables fresh
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()
Post.query.delete()

#add users
roger = User(first_name='Roger', 
             last_name='Everett')

mary = User(first_name='Mary', 
            last_name='Magdelene',
            image_url='https://images.pexels.com/photos/5491144/pexels-photo-5491144.jpeg?auto=compress&cs=tinysrgb&w=1600')

kerry = User(first_name='Kerry',
             last_name='Zhang',
             image_url='https://images.pexels.com/photos/3408354/pexels-photo-3408354.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2')

# add posts


# Add new objets to session, so they'll persist
db.session.add(roger)
db.session.add(mary)
db.session.add(kerry)

# Commit
db.session.commit()


