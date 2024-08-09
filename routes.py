from flask import render_template, request, redirect, url_for, flash
from werkzeug.security import check_password_hash
from flask_login import login_user, login_required
from models import db, User, Score

def register_routes(app):
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            hashed_password = generate_password_hash(password, method='sha256')

            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('login'))

        return render_template('register.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username).first()

            if user and check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('dashboard'))

            flash('Invalid username or password', 'error')

        return render_template('login.html')

    @app.route('/dashboard')
    @login_required
    def dashboard():
        # ... Dashboard route ...
        return render_template('dashboard.html')
