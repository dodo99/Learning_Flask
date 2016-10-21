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

#@app.route('/home')
#def home():
#    """Renders the home page."""
#    return render_template(
#        'index.html',
#        title='Home Page',
#        year=datetime.now().year,
#    )

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

    #places = []
    places = [{'url': u'http://en.wikipedia.org/wiki/Googleplex', 'lat': 37.422, 'lng': -122.084, 'name': u'Googleplex', 'time': 0}, {'url': u'http://en.wikipedia.org/wiki/Genetic_Information_Research_Institute', 'lat': 37.4193, 'lng': -122.088, 'name': u'Genetic Information Research Institute', 'time': 5}, {'url': u'http://en.wikipedia.org/wiki/Shoreline_Park,_Mountain_View', 'lat': 37.427, 'lng': -122.08537, 'name': u'Shoreline Park, Mountain View', 'time': 6}, {'url': u'http://en.wikipedia.org/wiki/Android_lawn_statues', 'lat': 37.41829, 'lng': -122.08782, 'name': u'Android lawn statues', 'time': 6}, {'url': u'http://en.wikipedia.org/wiki/Bridge_School_Benefit', 'lat': 37.426666666667, 'lng': -122.08083333333, 'name': u'Bridge School Benefit', 'time': 7}, {'url': u'http://en.wikipedia.org/wiki/Shoreline_Amphitheatre', 'lat': 37.426778, 'lng': -122.080733, 'name': u'Shoreline Amphitheatre', 'time': 7}, {'url': u'http://en.wikipedia.org/wiki/CyberSource', 'lat': 37.42, 'lng': -122.075, 'name': u'CyberSource', 'time': 10}, {'url': u'http://en.wikipedia.org/wiki/Rengstorff_House', 'lat': 37.431455555556, 'lng': -122.0871, 'name': u'Rengstorff House', 'time': 12}, {'url': u'http://en.wikipedia.org/wiki/VirtualPBX', 'lat': 37.4201, 'lng': -122.0728, 'name': u'VirtualPBX', 'time': 13}, {'url': u'http://en.wikipedia.org/wiki/MIPS_Technologies', 'lat': 37.4201, 'lng': -122.0728, 'name': u'MIPS Technologies', 'time': 13}, {'url': u'http://en.wikipedia.org/wiki/Computer_History_Museum', 'lat': 37.414371, 'lng': -122.076817, 'name': u'Computer History Museum', 'time': 13}, {'url': u'http://en.wikipedia.org/wiki/Intuit', 'lat': 37.427222222222, 'lng': -122.09638888889, 'name': u'Intuit', 'time': 14}, {'url': u'http://en.wikipedia.org/wiki/Permanente_Creek', 'lat': 37.433333333333, 'lng': -122.08583333333, 'name': u'Permanente Creek', 'time': 15}, {'url': u'http://en.wikipedia.org/wiki/Kehillah_Jewish_High_School', 'lat': 37.4249, 'lng': -122.1045, 'name': u'Kehillah Jewish High School', 'time': 22}, {'url': u'http://en.wikipedia.org/wiki/Ames_Research_Center', 'lat': 37.415229, 'lng': -122.06265, 'name': u'Ames Research Center', 'time': 25}, {'url': u'http://en.wikipedia.org/wiki/Singularity_University', 'lat': 37.415229, 'lng': -122.06265, 'name': u'Singularity University', 'time': 25}, {'url': u'http://en.wikipedia.org/wiki/Unitary_Plan_Wind_Tunnel_(Mountain_View,_California)', 'lat': 37.416916666667, 'lng': -122.060475, 'name': u'Unitary Plan Wind Tunnel (Mountain View, California)', 'time': 27}, {'url': u'http://en.wikipedia.org/wiki/Saint_Athanasius_Parish', 'lat': 37.4043196, 'lng': -122.0968184, 'name': u'Saint Athanasius Parish', 'time': 28}, {'url': u'http://en.wikipedia.org/wiki/Charleston_Slough', 'lat': 37.441, 'lng': -122.096, 'name': u'Charleston Slough', 'time': 28}, {'url': u'http://en.wikipedia.org/wiki/NASA_Ames_Exploration_Center', 'lat': 37.408611111111, 'lng': -122.06444444444, 'name': u'NASA Ames Exploration Center', 'time': 29}]
    my_coordinates = (37.4223664, -122.084406)

    if request.method == 'POST':
        if form.validate() == False:
            return render_template(
                'home.html',
                form=form
            )
        else:
            #get the address
            address = form.address.data

            #query for palces around it
            #p = Place()
            #my_coordinates = p.address_to_latlng(address)
            #places = p.query(address)

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

