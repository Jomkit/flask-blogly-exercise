"""Blogly application."""

from flask import Flask, render_template, redirect, request, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag

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
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template('home.html', posts=posts)

@app.errorhandler(404)
def not_found(e):
    return render_template('not-found.html'), 404

########### USER ROUTES ############
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

    flash('User updated!', 'success')

    return redirect('/users')

@app.route('/users/<int:user_id>/delete')
def delete_user(user_id):
    User.query.get_or_404(user_id)
    User.query.filter_by(id=user_id).delete()
    db.session.commit()

    flash('User Deleted!','danger')
    
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

    flash('New user created!', 'success')

    return redirect('/users')

############### POSTS ##################

@app.route('/users/<int:user_id>/posts/new')
def show_new_post_form(user_id):
    """Show post form with title, content, and author. Include cancel, edit, and delete"""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()

    return render_template('new-post-form.html', user=user, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def create_new_post_form(user_id):
    """Create new post associated with user, redirect to 
       associated user's page"""
    title = request.form['title']
    content = request.form['content']
    tag_ids = request.form.getlist('tag')
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    new_post = Post(title=title,
                    content=content,
                    user_id=user_id,
                    tags=tags)

    db.session.add(new_post)
    db.session.commit()

    flash('Posted!','success')
    
    return redirect(f'/users/{user_id}')

@app.route('/posts/<post_id>')
def show_post(post_id):
    """Shows details of one post"""
    post = Post.query.get_or_404(post_id)

    return render_template('post-details.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def show_post_edit_form(post_id):

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    
    return render_template('edit-post.html', post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post(post_id):
    """Need to fix post edit to remove tags when they are unchecked"""
    
    post = Post.query.get_or_404(post_id)
    title = request.form['title']
    content = request.form['content']

    tag_ids = request.form.getlist('tag')
    # Get current list of tags by tag_ids from the edit form
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all() 
    
    post.title = title
    post.content = content
    post.tags = tags

    db.session.add(post)
    db.session.commit()

    flash('Post updated!','success')
    
    return redirect(f'/posts/{post_id}')

@app.route('/posts/<int:post_id>/delete')
def delete_post(post_id):
    
    post = Post.query.filter_by(id=post_id).delete()
    db.session.commit()

    flash('Post deleted!', 'danger')
    
    return redirect(f'/users')

############### tag routes ###############
@app.route('/tags')
def all_tags():
    tags = Tag.query.all()
    
    return render_template('tags.html',tags=tags)

@app.route('/tags/<tag_id>')
def tag_details(tag_id):
    tag = Tag.query.get_or_404(tag_id)

    return render_template('tag-details.html', tag=tag)

@app.route('/tags/new')
def new_tag_form():
    """Show form for making new tag"""
    all_posts = Post.query.all()
    return render_template('new-tag-form.html', all_posts=all_posts)

@app.route('/tags/new', methods=['POST'])
def create_new_tag():
    """
    Create new tag, redirect to all tags
    Trying to enter a new tag results in duplicate tag flash msg
    """
    check_name = request.form['name']

    if not Tag.query.filter_by(name=check_name).all() == []:
        flash('Tag already exists!', 'warning')
        return redirect('/tags')
    
    post_ids = request.form.getlist('post')
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name=check_name,
                  posts=posts)

    db.session.add(new_tag)
    db.session.commit()

    flash('Tag added!', 'success')

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit')
def tag_edit_form(tag_id):

    tag = Tag.query.get_or_404(tag_id)
    all_posts = Post.query.all()
    
    return render_template('edit-tag.html', tag=tag, all_posts=all_posts)

@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def edit_tag(tag_id):
    
    tag = Tag.query.get_or_404(tag_id)
    name = request.form['name']
    post_ids = request.form.getlist('post')
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()
    
    tag.name = name

    db.session.add(tag)
    db.session.commit()

    flash('Tag updated!','success')
    
    return redirect(f'/tags/{tag_id}')

@app.route('/tags/<int:tag_id>/delete')
def delete_tag(tag_id):
    
    Tag.query.filter_by(id=tag_id).delete()
    db.session.commit()

    flash('Tag deleted!', 'danger')
    
    return redirect('/tags')

