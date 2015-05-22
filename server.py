"""HB Spring 2015 Final project."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Position, Documents, Notes


app = Flask(__name__)

app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    return render_template("welcomepage.html")


@app.route('/dashboard')
def dashboard():
    """Dashboard."""
    my_user = session["user_id"]
    user = User.query.filter_by(user_id=my_user).one()
    positions = Position.query.filter_by(user_id=my_user).all()
    return render_template("dashboard.html", user=user, positions=positions)


@app.route('/register', methods=['GET'])
def registration():
    """Show form for user signup."""

    return render_template("register_form.html")


@app.route('/submit_register', methods=['POST'])
def process_registration():
    """Adds a new user to the database"""

    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    password = request.form.get("password")
    picture = request.form.get("picture")
    email_address = request.form.get("email_address")
    linkedin_url = request.form.get("linkedin_url")
    twitter_url = request.form.get("twitter_url")
    facebook_url = request.form.get("facebook_url")
    website_url = request.form.get("website_url")

    new_user = User.query.filter_by(email_address=email_address).first()
    if new_user:  #if the user's email already exists on file
        flash("This email address is already on file. Please log in!")
        return redirect('/login')
    else:
        new_user = User(first_name=first_name, last_name=last_name, password=password, picture=picture, email_address=email_address, linkedin_url=linkedin_url, twitter_url=twitter_url, facebook_url=facebook_url, website_url=website_url)

    db.session.add(new_user)
    db.session.commit()

    session["new_user"] = first_name

    flash("Thanks %s for joining the hunt!" % session["new_user"])
    return redirect('/login')


@app.route('/login', methods=['GET'])
def login_form():
    """Show login form."""

    return render_template("login_form.html")


@app.route('/login', methods=['POST'])
def login_process():
    """Process login."""

    email_address = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(email_address=email_address).first()

    if not user:
        return redirect('/login')

    if user.password != password:
        flash("Incorrect password")
        return redirect('/login')

    session["user_id"] = user.user_id

    flash("Logged in")
    return redirect('/dashboard')


@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]

    flash("Logged Out. Thanks for using The Hunt!")
    return redirect("/")


@app.route('/position')
def position_page():
    """Display user's position."""
    return render_template("positions.html")


@app.route('/submit_position', methods=['POST'])
def position_form():
    """Process a user's position."""
    title = request.form["title"]
    position_summary = request.form["position_summary"]
    deadline = request.form["deadline"]
    company_name = request.form["company_name"]
    location = request.form["location"]
    application_status = request.form["status"]
    position_url = request.form["position_url"]

    new_position = Position(title=title, position_summary=position_summary, deadline=deadline, company_name=company_name, location=location, application_status=application_status, position_url=position_url)

    db.session.add(new_position)
    db.session.commit()

    flash("Position %s added!" % title)
    return redirect("/listofpositions")


@app.route("/listofpositions")
def position_list():
    """Shows list of positions."""
    #I need to add code here that prompts a user to upload new positions
    #if there are no positions listed
    u = session["user_id"]
    my_user = User.query.filter_by(user_id=u).one()
    print my_user
    positions = my_user.positions
    return render_template("position_list.html", positions=positions)


@app.route("/position/<int:position_id>")
def position(position_id):
    """Shows info about a position."""
    position = Position.query.get(position_id)
    print position
    return render_template("position.html", position=position)


@app.route('/documents')
def documents_page():
    """This will show the a page for an user's positions."""
    return render_template("documents.html")


@app.route('/submit_documents', methods=['POST'])
def document_form():
    """Process a user's documents."""
    document_type = request.form["document_type"]
    document_content = request.form["document"]

    new_document = Documents(document_type=document_type, document_content=document_content)

    db.session.add(new_document)
    db.session.commit()

    flash("Your %s has been added!" % document_type)
    return redirect('/documents')


@app.route("/listofdocuments")
def document_list():
    """Shows list of documents."""
    documents = Documents.query.all()
    print documents
    return render_template("document_list.html", documents=documents)


@app.route("/document/<int:user_asset_id>")
def document(user_asset_id):
    """Shows info about a position."""
    document = Documents.query.get(user_asset_id)
    print document
    return render_template("document.html", document=document)


@app.route('/notes')
def notes_page():
    """This will show the a page for an user's notes."""
    return render_template("notes.html")


@app.route('/submit_notes', methods=['POST'])
def note_form():
    """Process a user's notes."""
    note_type = request.form["note_type"]
    note_details = request.form["note_details"]

    new_note = Notes(note_type=note_type, note_details=note_details)

    db.session.add(new_note)
    db.session.commit()

    flash("Your %s has been added!" % note_type)
    return redirect("/listofnotes")


@app.route("/listofnotes")
def note_list():
    """Shows list of notes."""
    notes = Notes.query.all()
    print notes
    return render_template("note_list.html", notes=notes)


@app.route("/notes/<int:note_id>")
def note(note_id):
    """Shows info about a note."""
    note = Notes.query.get(note_id)
    print note
    return render_template("note.html", note=note)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run()
