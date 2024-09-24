from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret123'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

with app.app_context():
    db.create_all()

    new_user = User(first_name="John", last_name="Doe", image_url="https://via.placeholder.com/150")
    db.session.add(new_user)
    db.session.commit()

@app.route("/")
def user_list():
    users = User.query.all()
    return render_template("user_list.html", users=users)

@app.route("/new-user")
def new_user():
    return render_template("new_user.html")

@app.route("/new-user", methods=["POST"])
def add_new_user():
    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'])

    db.session.add(new_user)
    db.session.commit()

    return redirect("/")

@app.route("/user-details/<int:user_id>")
def user_details(user_id):
    user = User.query.get(user_id)
    return render_template("user_details.html", user=user)

@app.route("/user-edit/<int:user_id>")
def edit_user_form(user_id):
    user = User.query.get(user_id)
    return render_template("edit_user.html", user=user)

@app.route("/user-edit/<int:user_id>", methods=["POST"])
def submit_edit_user(user_id):
    user = User.query.get(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.commit()

    return redirect("/")

@app.route("/user-delete/<int:user_id>", methods=["POST"])
def delete_user(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/")