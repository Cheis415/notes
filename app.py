from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User
from forms import RegisterForm, LoginForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///notes_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "poopybutt420"

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)


@app.route("/")
def homepage():
    """Show homepage with links to site areas."""

    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user: produce form & handle form submission."""

    form = RegisterForm()

    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data
        email = form.email.data
        fn = form.first_name.data
        ln = form.last_name.data

        user = User.register(name, pwd, email, fn, ln)
        db.session.add(user)
        db.session.commit()

        session["user_id"] = user.id

        # on successful login, redirect to secret page
        return redirect("/user/{{user.name}}")

    else:
        return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Produce login form or handle login."""

    form = LoginForm()

    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data

        # authenticate will return a user or False
        user = User.authenticate(name, pwd)

        if user:
            session["user_id"] = user.id  # keep logged in
            return redirect("/user/user_id")

        else:
            form.username.errors = ["Don't mess with the Zohan."]

    return render_template("login.html", form=form)


@app.route("/user/<username>")
def user_page(username):
    """Example hidden page for logged-in users only."""
    user = User.query.get_or_404(username)
    if "user_id" not in session:
        flash("You are not permitted here idiot!")
        return redirect("/")

    else:
        flash("You made it!  Ezpzlemonsqzy.")
        return render_template("user.html", user=user)


@app.route("/logout")
def logout():
    """Logs user out and redirects to homepage."""

    session.pop("user_id")

    return redirect("/")

@app.route("/user/<username>/delete",methods=["POST"])
def delete_user():
    """deletes user from database"""
    user = User.query.get_or_404(username)
    db.session.delete(user)
    db.session.commit()
    return redirect('/')

@app.route("/user/<username>/notes/add", methods=["POST"])
def add_note(username):
    """adds note to user"""
    form = AddNoteForm()
    user = User.query.get_or_404(username)
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        owner = user.id
        note = Note(title, content, owner)
        db.session.add(note)
        db.session.commit()
        # adds a new note
        return redirect(url_for('user', username=user.username))

    else:
        return render_template("note_add.html", form=form)

@app.route("/user/<username>/notes/<int:note_id>/update", methods=["GET","POST"])
def update_note(username, note_id)
    """updates note for user"""
    form = AddNoteForm()
    note = Note.query.get_or_404(note_id)
    if form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data
        db.session.commit()
        # updates the note
        return redirect(url_for('user', username=user.username))

    else:
        return render_template("note_add.html", form=form)


@app.route("/user/<username>/notes/<int:note_id>/delete", methods=["POST"])
def user_note(username,note_id):
    """deletes note from database"""
    user = User.query.get_or_404(username)
    note = Note.query.get_or_404(note_id)
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for('user', username=user.username, note_id=note.id))
)
