from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret123'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

with app.app_context():
    # db.drop_all()
    db.create_all()

    new_user = User(first_name="John", last_name="Doe", image_url="https://via.placeholder.com/150")
    db.session.add(new_user)
    db.session.commit()

@app.route("/")
def user_list():
    """show the user list"""
    users = User.query.all()
    return render_template("user_list.html", users=users)

@app.route("/new-user")
def new_user():
    """show the new user form"""
    return render_template("new_user.html")

@app.route("/new-user", methods=["POST"])
def add_new_user():
    """handles submit of new user form, updates DB and redirect to user list page"""
    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'])

    db.session.add(new_user)
    db.session.commit()

    return redirect("/")

@app.route("/user-details/<int:user_id>")
def user_details(user_id):
    """show the user detail page"""
    user = User.query.get(user_id)
    return render_template("user_details.html", user=user)

@app.route("/user-edit/<int:user_id>")
def edit_user_form(user_id):
    """show the edit user page with their data in the form fields."""
    user = User.query.get(user_id)
    return render_template("edit_user.html", user=user)

@app.route("/user-edit/<int:user_id>", methods=["POST"])
def submit_edit_user(user_id):
    """handle the submit of edit user, updates DB with new info, redirect to user list"""
    user = User.query.get(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.commit()

    return redirect("/")

@app.route("/user-delete/<int:user_id>", methods=["POST"])
def delete_user(user_id):
    """handle the submit of delete button, deletes record on DB, redirect to user list"""
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/")

@app.route("/user/<int:user_id>/new-post")
def post_form(user_id):
    """show the new post form page"""
    user = User.query.get(user_id)
    tags = Tag.query.all()
    return render_template("new_post_form.html", user=user, tags=tags)

@app.route("/user/<int:user_id>/new-post", methods=["POST"])
def submit_post_form(user_id):
    """handle the submit of the new post with optional tags."""
    user = User.query.get(user_id)

    new_post = Post(title=request.form['title'],
                    content=request.form['content'],
                    user=user)

    db.session.add(new_post)

    selected_tag_ids = request.form.getlist('tags')

    if selected_tag_ids:
        tags = Tag.query.filter(Tag.id.in_(selected_tag_ids)).all()
        new_post.tags.extend(tags)

    db.session.commit()

    return render_template("user_details.html", user=user)

@app.route("/posts/<int:post_id>")
def show_post(post_id):
    """show the post detail page"""
    post = Post.query.get_or_404(post_id)
    return render_template("post_detail.html", post=post)

@app.route("/posts/<int:post_id>", methods=["POST"])
def delete_post(post_id):
    """handle the submit delete from the post detail page"""
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(f"/user-details/{post.user_id}")

@app.route("/posts/<int:post_id>/edit")
def edit_post(post_id):
    """show the edit post page"""
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template("edit_post.html", post=post, tags=tags)

@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def submit_edit_post(post_id):
    """handle the submit of edit post"""
    post = Post.query.get_or_404(post_id)

    post.title = request.form['title']
    post.content = request.form['content']

    selected_tag_ids = request.form.getlist('tags')
    post.tags.clear()

    if selected_tag_ids:
        selected_tags = Tag.query.filter(Tag.id.in_(selected_tag_ids)).all()
        post.tags.extend(selected_tags)

    db.session.commit()
    return render_template("post_detail.html", post=post)

@app.route("/tags")
def show_tags_page():
    tags = Tag.query.all()
    return render_template("tags_page.html", tags=tags)

@app.route("/tags/new")
def create_tag_form():
    return render_template("create_tag.html")

@app.route("/tags/new", methods=["POST"])
def submit_tag_form():
    tag_name = request.form.get("tag_name")
    new_tag = Tag(name=tag_name)
    db.session.add(new_tag)
    db.session.commit()
    return redirect("/tags")

@app.route("/tags/<int:tag_id>")
def tag_details(tag_id):
    """show the tag details page"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template("/tag_details.html", tag=tag)

@app.route("/tags/<int:tag_id>/edit")
def edit_tag_page(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template("edit_tag_form.html", tag=tag)

@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def submit_edit_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)

    new_tag_name = request.form['name']
    tag.name = new_tag_name

    db.session.commit()

    return redirect(f"/tags/{tag.id}")