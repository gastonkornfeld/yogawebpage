from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import models
# this two ones are for secure the password
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, forms
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login route of the app. 
    """
    form = forms.LoginForm()
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = models.User.query.filter_by(email=email).first()
        if user:
            # this is the line that checks if the password match the hash built in
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True) #log in the user
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='danger')
        else:
            flash('Email does not exist.', category='danger')

    return render_template("login.html", user=current_user, form = form)


@auth.route('/logout')
@login_required
def logout():
    """
    Logout route of the app
    """ 
    logout_user()
    return redirect(url_for('views.home'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    This route is only for administration use. To create new students in to the yoga school.

    """
    form = forms.RegisterStudentForm()
    if request.method == 'POST':
        email = form.email.data
        name = form.name.data
        username = form.username.data
        password1 = form.password1.data
        password2 = form.password2.data
        other_info = form.other_info.data

        user = models.User.query.filter_by(email=email).first()
        user2 = models.User.query.filter_by(username=username).first()
        if user:
            flash('Email already exists. (Email Existente)', category='danger')
        elif user2:
            flash('Username already exists. (El nombre de usuario Ya existe)', category='danger')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='danger')
        elif len(name) < 2:
            flash('Name must be greater than 1 character.', category='danger')
        elif password1 != password2:
            flash('Passwords don\'t match. (La contrasena no coincide)', category='danger')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters. (Contrasena minimo 7 characteres', category='danger')
        else:
            # create the user in the database
            # note the password was generate using the generate password hash
            new_user = models.User(email=email, name= name, username = username, other_info = other_info,  password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            # login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("register_student.html", user=current_user, form = form)