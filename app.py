"""Blogly application."""

from flask import Flask, render_template, request, redirect, flash, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, app, connect_db, User, Post
from IPython import embed
import datetime

app.config['SECRET_KEY'] = "secretsecret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)
# with app.app_context():
#     db.create_all()

def get_timestamp():
    date = datetime.datetime.today()
    day = date.strftime("%m/%d/%Y")
    time = date.strptime(date.strftime("%H:%M"), '%H:%M').strftime('%I:%M %p')
    return f"{day} {time}"

@app.route('/')
def homepage():
    return redirect('/users')

@app.route('/users')
def userpage():
    """Showing homepage"""
    users = User.query.all()
    embed()
    return render_template('/home.html', users = users)

@app.route('/users/new')
def user_form():
    return render_template('/newuser.html')

@app.route('/users/new', methods=['POST'])
def submit_user():
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
    user = User.query.get_or_404(user_id)
    return render_template('/user-details.html', user = user)

@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    # print(user)
    return render_template('/edit-user.html', user = user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def submit_edit(user_id):
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
    User.query.filter(User.id == user_id).delete()
    db.session.commit()
    return redirect('/users')
    