'''
Wilson Holmes
Created: 2020/05/04
Last Modified: 2020/05/04
Description: Flask powered blog, using bootstrap classes and a SQLite3 database to store user accounts and blog articles
'''

# Imports
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from data import Articles
import sqlite3
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import pbkdf2_sha256
from functools import wraps

app = Flask(__name__)

# Provides dummy articles for now
Articles = Articles()

# Home page
@app.route('/')
def index():
    return render_template('home.html')

# About page
@app.route('/about')
def about():
    return render_template('about.html')

# Page to show all of the articles on the blog
@app.route('/articles')
def articles():
    return render_template('articles.html', articles = Articles)

# Page to show individual article from the database
@app.route('/article/<string:id>/')
def article(id):
    return render_template('article.html', id = id)

# WTForms class to handle the registration page's forms logic
class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')

# The registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = pbkdf2_sha256.hash(str(form.password.data))

        # Sets up the connection to the database
        sqlite_file = 'myflaskapp.db'
        conn = sqlite3.connect(sqlite_file)

        # Create Cursor
        cur = conn.cursor()

        # Execute query
        cur.execute("INSERT INTO users(name, email, username, password) VALUES(?, ?, ?, ?)", (name, email, username, password))

        # Commit to DB
        conn.commit()

        # Close connection
        conn.close()

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# User Login
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':

        # Get form fields (maybe change these later to be WTForms)
        username = request.form['username']
        password_candidate = request.form['password']

        # Sets up the connection to the database
        sqlite_file = 'myflaskapp.db'
        conn = sqlite3.connect(sqlite_file)

        # Create Cursor
        cur = conn.cursor()

        # Execute query/ get username
        cur.execute("SELECT * FROM users WHERE username = ?", (username,))

        # See if the data exits, if it does, then store the data into variable "data"
        data = cur.fetchone()

        # If user is found
        if data:
            # Get stored hash from the 4 column index in the database
            password = data[4]

            # Compare passwords
            if (pbkdf2_sha256.verify(password_candidate, password)):
                # Password is correct
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                # Password is not correct
                error = 'Login incorrect'
                return render_template('login.html', error=error)
            
            # Close connection
            conn.close()

        else:
            # The user is not registered
            error = 'There is no account with the username "{}"'.format(username)  # Username not found
            return render_template('login.html', error=error)

    return render_template('login.html')

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You cannot access that page as you are not logged in', 'danger')
            return redirect(url_for('login'))
    return wrap


# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

# Dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
    return render_template('dashboard.html')


if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)
