from flask import Blueprint, render_template, request, flash
from flask.helpers import url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.utils import redirect
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            flash('Logged in successfully!', category='success')
            login_user(user, remember=True)
            return redirect(url_for('views.home'))
        else:
            flash('Login failed, try again!', category='error')

    return render_template('login.html', user=current_user)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()

        # validations
        if user:
            flash('Email already exists', category='error')
        elif len(name.strip()) < 2:
            flash('Name must greater than 1 character.', category='error')
        elif len(email.strip()) < 7:
            flash('Email must greater than 6 characters.', category='error')
        elif password.strip() != password2.strip():
            flash('Password don\'t match.', category='error')
        elif len(password.strip()) < 5:
            flash('Password must at least 5 characters.', category='error')
        else:
            # craete user's account
            new_user = User(name=name, email=email, password=generate_password_hash(password, 'sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template('register.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    flash('Logged out successfully!', category='success')
    logout_user()
    return redirect(url_for('auth.login'))