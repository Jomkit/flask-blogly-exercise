"""Blogly application."""

from flask import Flask, render_template, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

"""Debugging stuff"""
app.config['SECRET_KEY'] = "secretcode123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def homepage():
    return redirect('/users')

@app.route('/users')
def show_users():
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users.html', users=users)

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Show user details: profile image, full name, and then
       edit and delete buttons"""
    user = User.query.get_or_404(user_id)

    return render_template('details.html', user=user)

@app.route('/users/<int:user_id>/edit')
def show_edit_form(user_id):

    user = User.query.get_or_404(user_id)
    
    return render_template('edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):
    
    user = User.query.get_or_404(user_id)
    f_name = request.form['firstName']
    l_name = request.form['lastName']
    image_url = request.form['imageUrl']
    image_url = image_url if image_url else None

    user.first_name = f_name
    user.last_name = l_name
    user.image_url = image_url

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return redirect('/users')

@app.route('/users/new')
def show_new_user_form():

    return render_template('new-user-form.html')

@app.route('/users/new', methods=['POST'])
def create_new_user_form():
    f_name = request.form['firstName']
    l_name = request.form['lastName']
    image_url = request.form['imageUrl']
    image_url = image_url if image_url else None

    new_user = User(first_name=f_name,
                    last_name=l_name,
                    image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

