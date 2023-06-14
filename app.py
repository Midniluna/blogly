"""Blogly application."""

from flask import Flask, render_template, request, redirect, flash, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post
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
    return redirect('/users')


@app.route('/users')
def userpage():
    """Showing homepage"""

    users = User.query.all()
    # embed()
    return render_template('/home.html', users = users)


@app.route('/users/new')
def user_form():
    """Shows a form to submit a new user"""

    return render_template('/newuser.html')


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
    return redirect('/users')


@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Get details about a user"""

    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id = user.id)
    # embed()
    return render_template('/user-details.html', user = user, posts = posts )


@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    """Shows a form to edit an existing user's details"""

    user = User.query.get_or_404(user_id)
    return render_template('/edit-user.html', user = user)


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
    return redirect(f'/users/{user_id}')


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Delete existing user"""

    User.query.filter(User.id == user_id).delete()
    db.session.commit()
    return redirect('/users')

# POSTS ROUTES
    
@app.route('/users/<int:user_id>/posts/new')
def new_post(user_id):
    """Shows form for new post"""
    user = User.query.get_or_404(user_id)
    # embed()
    return render_template("/new-post.html", user=user)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def create_post(user_id):
    """Submit new post"""

    title = request.form['title']
    content = request.form['content']
    date = datetime.datetime.today()
    new_post = Post(title=title, content=content, created_at=date, user_id=user_id)
    db.session.add(new_post)
    db.session.commit()
    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def view_post(post_id):
    post = Post.query.get_or_404(post_id)
    # embed()
    return render_template('view-post.html', post = post)

@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('edit-post.html', post = post)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def submit_post_edit(post_id):
    post = Post.query.get_or_404(post_id)
    title = request.form['title']
    content = request.form['content']
    post.title = title
    post.content = content
    db.session.commit()
    return redirect(f'/posts/{post_id}')

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(f'/users/{post.user_id}')