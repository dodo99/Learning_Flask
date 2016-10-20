"""
This script runs the Learning_Flask application using a development server.
"""

from os import environ
from Learning_Flask import app
from Learning_Flask.forms import SignupForm

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/learningflask'

app.secret_key = 'development-key'

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT, debug=True)
