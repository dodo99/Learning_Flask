"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request
from Learning_Flask import app
from Learning_Flask.forms import SignupForm
from Learning_Flask.models import db, User


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

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
            return 'Success!'
    elif request.method == 'GET':
        return render_template(
            'signup.html',
            form=form
        )   
