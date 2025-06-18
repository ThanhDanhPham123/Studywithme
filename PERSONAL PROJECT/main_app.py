#Import necessary libraries
from flask import Flask, render_template, url_for, request, redirect, session
from route.features.todo import todo 
from route.features.chat_with_bot import chat_bp  # Import the chat blueprint
from flask_sqlalchemy import SQLAlchemy
from db import db #Initialize the databse in another file to prevent circular imports
from functools import wraps
from auth import login_required # Use to make the user sign in before being able to access all the functions

# Initialize Flask app and database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SECRET_KEY'] = 'your_secret_key'

# User model and set up the database 
class User(db.Model): #Syntax used : db.Model to create a model for the database
    # db.Column is used to create a column in the database
    id = db.Column(db.Integer, primary_key=True) #Id column 
    username = db.Column(db.String(100), nullable=False) #User name column
    grad_year = db.Column(db.Integer, nullable=False) #Graduation year column
    purpose = db.Column(db.String(100), nullable=False) #Purpose column

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Create the form that the user will use to enter their information
        username = request.form["username"]
        grad_year = request.form["grad_year"]
        purpose = request.form["purpose"]
        # Create a ew user with the data added to the database
        new_user = User(username=username, grad_year=grad_year, purpose=purpose)
        db.session.add(new_user)
        db.session.commit()
        session['username'] = username  # Store username in session
        return redirect(url_for("index"))
    users = User.query.all()
    years = range(2025, 2036)
    username = session.get('username')  # Get username from session if exists
    return render_template('home.html', users=users, years=years, username=username)

#Handle user longging out
@app.route("/logout")
def logout():
    username = session.get('username') # Get the username from the session
    if username:
        user = User.query.filter_by(username=username).first() #Take the first user with the username
        # If the user exists, delete them from the database
        if user:
            db.session.delete(user)
            db.session.commit()
    session.clear()
    return redirect(url_for("index"))

app.register_blueprint(todo) # Register the todo blueprint
app.register_blueprint(chat_bp)  # Register the chat blueprint
db.init_app(app)  # Bind to app after creation

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)