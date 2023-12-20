"""Blogly application."""

from flask import Flask, render_template, redirect, request
from models import db, connect_db, USER
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'helloimasecret'

debug = DebugToolbarExtension(app)


connect_db(app)
with app.app_context():
    db.create_all()

@app.route('/')
def root():
    return redirect("/users")

@app.route('/users')
def user_page():
    users = USER.query.order_by(USER.last_name, USER.first_name).all()
    return render_template('user-page.html', users=users)

@app.route('/users/new', methods=["GET"])
def show_add_user_form():
    return render_template('add-user.html')

@app.route('/users/new', methods=["POST"])
def add_user():
    first_name = request.form['first-name']
    last_name = request.form['last-name']
    img_url = request.form['img-url'] or None
    
    new_user = USER(first_name=first_name, last_name=last_name, img_url=img_url)

    db.session.add(new_user)
    db.session.commit()
    return redirect('/users')

@app.route("/users/<int:id>")
def user_details(id):
    user = USER.query.get_or_404(id)
    return render_template('details.html', user=user)

@app.route('/users/<int:id>/edit', methods=["GET"])
def edit_user(id):
    user = USER.query.get_or_404(id)
    return render_template('edit-user.html', user=user)

@app.route('/users/<int:id>/edit', methods=["POST"])
def save_updated_user(id):
        user = USER.query.get_or_404(id)
        user.first_name = request.form['first-name']
        user.last_name = request.form['last-name']
        user.img_url = request.form['img-url']
        db.session.add(user)
        db.session.commit()
        return redirect('/users')

@app.route('/users/<int:id>/delete')
def delete_user(id):
    USER.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect('/users')