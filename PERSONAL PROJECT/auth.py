# This file contains the authentication logic for the Flask application.
# auth.py   
#Importing import necessary libraries
from flask import session, redirect, url_for
from functools import wraps

def login_required(f):
    @wraps(f) # This decorator is used to preserve the original function's name and docstring
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function