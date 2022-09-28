from dataclasses import dataclass
from flask import Flask, render_template, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet

from forms import AddPetForm, EditPetForm

app = Flask(__name__)
app.config['SECRET_KEY'] = "12345"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///pets"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_ECHO'] = True

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def homepage():
    """Show list of pets"""
    pets = Pet.query.all()

    return render_template('home.html', pets=pets)

@app.route('/add', methods=["GET", "POST"])
def add_page():
    """Show form to add pet; handle adding"""

    form = AddPetForm()

    if form.validate_on_submit():
        pet = Pet(name=form.name.data,
                    species=form.species.data,
                    photo_url=form.photo_url.data,
                    age=form.age.data,
                    notes=form.notes.data,
                    available=form.available.data)
        db.session.add(pet)
        db.session.commit()
        return render_template('home.html')
    else:
        return render_template('pet_form.html', form=form)

@app.route('/<int:petid>')
def show_pet(petid):
    """Show information about a pet"""
    
    pet = Pet.query.get_or_404(petid)

    return render_template('pet.html', pet=pet)

@app.route('/<int:petid>/edit', methods=["GET", "POST"])
def edit_page(petid):
    """Show form to edit pet; handle edit"""

    form = EditPetForm()

    if form.validate_on_submit():
        pet = Pet.query.get_or_404(petid)
        pet.notes = form.notes.data
        pet.available = form.available.data
        pet.photo_url = form.photo_url.data
        db.session.commit()
        return render_template('home.html')
    else:
        return render_template('edit_pet_form.html', form=form)