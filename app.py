"""Blogly application."""

from flask import Flask, render_template, request, redirect, flash, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag
from IPython import embed
import datetime

app = Flask(__name__)

# app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

app.config['SECRET_KEY'] = "secretsecret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)

def get_timestamp():
    date = datetime.datetime.today()
    day = date.strftime("%m/%d/%Y")
    time = date.strptime(date.strftime("%H:%M"), '%H:%M').strftime('%I:%M %p')
    return f"{day} {time}"

# HOME + USERS ROUTES


@app.route('/')
def homepage():
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template('home.html', posts=posts)


@app.route('/users')
def userpage():
    """Showing homepage"""

    users = User.query.all()
    # embed()
    return render_template('users/users.html', users = users)


@app.route('/users/new')
def user_form():
    """Shows a form to submit a new user"""

    return render_template('users/new-user.html')


@app.route('/users/new', methods=['POST'])
def submit_user():
    """Submit a new user"""

    fname = request.form['firstname']
    lname = request.form['lastname']
    url = request.form['imgurl']
    if len(fname) == 0 or len(lname) == 0:
        flash('Please enter a valid name')
    else:
        new_user = User(first_name=fname, last_name=lname, img_url=url)
        db.session.add(new_user)
        db.session.commit()
    return redirect('users/users')


@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Get details about a user"""

    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id = user.id)
    # embed()
    return render_template('users/user-details.html', user = user, posts = posts )


@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    """Shows a form to edit an existing user's details"""

    user = User.query.get_or_404(user_id)
    return render_template('users/edit-user.html', user = user)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def submit_edit(user_id):
    """Submit edited user info"""

    fname = request.form['firstname']
    lname = request.form['lastname']
    url = request.form['imgurl']
    if len(fname) == 0 or len(lname) == 0:
        flash('Please enter a valid name')
        return redirect(f'/users/{user_id}/edit')
    else:
        user = User.query.get_or_404(user_id)
        user.first_name = fname
        user.last_name = lname
        user.img_url = url
        db.session.commit()
    return redirect(f'users/users/{user_id}')


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Delete existing user"""

    User.query.filter(User.id == user_id).delete()
    db.session.commit()
    return redirect('users/users')

# POSTS ROUTES
    
@app.route('/users/<int:user_id>/posts/new')
def new_post(user_id):
    """Shows form for new post"""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    # embed()
    return render_template("posts/new-post.html", user=user, tags=tags)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def create_post(user_id):
    """Submit new post"""
    title = request.form['title']
    content = request.form['content']
    # embed()
    tag_ids = [int(num) for num in request.form.getlist('tag')]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    date = datetime.datetime.today()
    new_post = Post(title=title, content=content, created_at=date, user_id=user_id, tag=tags)  

    db.session.add(new_post)
    db.session.commit()
    print("Success")

    # title = request.form['title']
    # content = request.form['content']
    # date = datetime.datetime.today()
    # new_post = Post(title=title, content=content, created_at=date, user_id=user_id)
    # db.session.add(new_post)
    # db.session.commit()
    return redirect(f'/users/{user_id}')

@app.route('/posts')
def view_posts():
    """Render list of all posts"""

    posts = Post.query.all()

    return render_template('posts/posts.html', posts=posts)


@app.route('/posts/<int:post_id>')
def view_post(post_id):
    """Render post details page"""

    post = Post.query.get_or_404(post_id)
    return render_template('posts/view-post.html', post = post)

@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    """Render post edit form"""

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('posts/edit-post.html', post = post, tags=tags)


@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def submit_post_edit(post_id):
    """Submit edited post"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    tag_ids = [int(num) for num in request.form.getlist('tag')]
    post.tag = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()
    return redirect(f'/posts/{post_id}')


@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """Delete a post"""

    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(f'/users/{post.user_id}')

# Same tag name gives IntegrityError (give error "this tag already exists")
# upper('text here') uppercases first letter, rest lowercase

# TAG ROUTES

@app.route('/tags')
def list_tags():
    """Generate list of tags"""

    tags = Tag.query.all()
    return render_template('tags/tags.html', tags = tags)


@app.route('/tags/<int:tag_id>')
def view_tag(tag_id):
    """Get data about a single tag"""

    tag = Tag.query.get_or_404(tag_id)
    return render_template('tags/tags-about.html', tag=tag)


@app.route('/tags/new')
def make_tag():
    """Render form to submit a new tag"""

    return render_template('tags/new-tag.html')


@app.route('/tags/new', methods=["POST"])
def submit_tag():
    """Handle submission of new tag"""

    tag_name = request.form['name'].capitalize()

    # Make sure tag name isn't blank
    if tag_name == "":
        flash("Please fill in the field")
        return redirect('/tags/new')

    new_tag = Tag(name=tag_name)

    # If tag name already exists, redirect and flash an error message
    try:
        db.session.add(new_tag)
        db.session.commit()
    except:
        db.session.rollback()
        flash("Tag name already exists")
        return redirect('/tags/new')

    return redirect('/tags')


@app.route('/tags/<int:tag_id>/edit')
def edit_tag(tag_id):
    """Render form to edit tag"""
    
    tag = Tag.query.get_or_404(tag_id)

    return render_template('tags/edit-tag.html', tag=tag)


@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def submit_tag_edit(tag_id):
    """Handle tag edit submission"""

    
    tag = Tag.query.get_or_404(tag_id)
    name = request.form['name'].capitalize()

    # Make sure tag name isn't blank
    if name == "":
        flash("Please fill in the field")
        return redirect('/tags/new')

    tag.name = name

    # If tag name already exists, redirect and flash an error message
    try:
        db.session.commit()
    except:
        db.session.rollback()
        flash("Tag name already exists")
        return redirect(f'/tags/{tag_id}/edit')

    return redirect(f'/tags/{tag_id}')


@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
    """Handle tag edit submission"""

    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()

    return redirect('/tags')
