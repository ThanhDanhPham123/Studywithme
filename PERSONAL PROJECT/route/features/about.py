from flask import Flask, render_template, url_for, request, redirect, session,Blueprint
 # Import the chat blueprint
from flask_sqlalchemy import SQLAlchemy
from db import db #Initialize the databse in another file to prevent circular imports
from functools import wraps
from auth import login_required # Use to make the user sign in before being able to access all the functions

about_bp = Blueprint("about", __name__, )
@about_bp.route("/about_and_contact")
@login_required
def about():
    username = session.get('username')  # Get username from session if exists
    return render_template('about.html', username=username)