"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request, session, redirect, url_for
from Learning_Flask import app
from Learning_Flask.forms import SignupForm, LoginForm, AddressForm
from Learning_Flask.models import db, User, Place


@app.route('/')
def index():
  return render_template("index.html")

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

db.init_app(app)

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if 'email' in session:
        return redirect(url_for('home'))

    form = SignupForm()
    if request.method == 'POST':
        if form.validate() == False:
            return render_template(
                'signup.html',
                form=form
            )
        else:
            newuser = User(form.first_name.data, form.last_name.data, form.email.data, form.password.data)
            db.session.add(newuser)
            db.session.commit()

            session['email'] = newuser.email
            return redirect(url_for('home'))
    elif request.method == 'GET':
        return render_template(
            'signup.html',
            form=form
        )   

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if 'email' in session:
        return redirect(url_for('home'))

    form = LoginForm()
    if request.method == 'POST':
        if form.validate() == False:
            return render_template(
                'login.html',
                form=form
            )
        else:
            email = form.email.data
            password = form.password.data

            user = User.query.filter_by(email=email).first()
            if user is not None and user.check_password(password):
                session['email'] = form.email.data
                return redirect(url_for('home'))
            else:
                return redirect(url_for('login'))
    elif request.method == 'GET':
        return render_template(
            'login.html',
            form=form
        )   

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))


@app.route('/home', methods = ['GET', 'POST'])
def home():
    if 'email' not in session:
        return redirect(url_for('login'))

    form = AddressForm()

    places = []
    # my_coordinates = p.address_to_latlng("Prudential tower Boston")
    my_coordinates = (42.3471426, -71.0825182)

    if request.method == 'POST':
        if form.validate() == False:
            return render_template(
                'home.html',
                form=form
            )
        else:
            #get the address
            address = form.address.data
            #if address is None:
            #    adress = 'Prudential tower Boston'

            #query for palces around it
            p = Place()
            my_coordinates = p.address_to_latlng(address)
            places = p.query(address)

            #return those results
        return render_template(
            'home.html',
            form=form,
            my_coordinates= my_coordinates,
            places=places
        )
    elif request.method == 'GET':
        return render_template(
            'home.html',
            form=form,
            my_coordinates= my_coordinates,
            places=places
        )

