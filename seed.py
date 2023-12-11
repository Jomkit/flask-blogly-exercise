from models import User, Post, db 
from app import app
from datetime import datetime

# cr 12, 11, 13, 12, 44eate all tables fresh
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
p1 = Post(title="I'm Roger", content="Hi, it's me Roger", user_id=1, created_at=datetime(2023, 12, 10, 18, 12, 44))
p2 = Post(title="Not Roger", content="Hey I'm Mary", user_id=2, created_at=datetime(2023, 12, 11, 13, 12, 44))
p3 = Post(title="Love Dogs", content="I'm Kerry, and I love dogs", user_id=3)
p4 = Post(title="I'm Roger's Mom", content="This is Roger's mom, can someone tell him it's dinner time?", user_id=1, created_at=datetime(2023, 12, 11, 9, 12, 44))
p5 = Post(title="Account Security", content="Make sure to log out securely every time you're done posting. -Mary", user_id=2)
p6 = Post(title="Ooops", content="That was an accident haha", user_id=1)

# Add new objets to session, so they'll persist
db.session.add(roger)
db.session.add(mary)
db.session.add(kerry)

db.session.commit()

db.session.add(p1)
db.session.add(p2)
db.session.add(p3)
db.session.add(p4)
db.session.add(p5)
db.session.add(p6)

db.session.commit()


