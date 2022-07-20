from flask import Blueprint, render_template, request, flash, redirect, url_for
from .DBModels import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth',__name__)


@auth.route("/login", methods=["POST","GET"])
def login():
    print(request.method)
    if request.method == "POST":
        print("AA")
        email = request.form.get('email')
        pwd = request.form.get('password')
        print("BBj")

        user = User.query.filter_by(email=email).first()
        print(user)

        if user:
            print("CC")
            if check_password_hash(user.password,pwd):
                print("DD")
                flash('Logged in successfully',category='sucess')
                login_user(user,remember=True)
                print("logged in")
                return redirect(url_for('views.dashboard'))
            else:
                flash('Incorrect Password, please try again',category='error')
        else:
            flash('Email does not exist',category='error')

    return render_template('login.html',user=current_user)


@auth.route("/logout",methods=["POST","GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))




@auth.route('/sign-up', methods=['GET','POST'])
def sign_up():
    print(request.method)
    if request.method == 'POST':
        print(request)
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        #user = User.query.filter_by(email=email).first()
        #if user:
        #    flash('Email already exists',category='error')
        #    print("a")
        if len(email) < 4:
            flash('Email must be greater than 4 chars',category='error')
            print("b")
        elif len(first_name) < 2:
            flash('Fairst names must be longer than 2 chars',category='error')
            print("c")
        elif password1 != password2:
            flash('Passwords dont match',category='error')
            print("d")
        elif len(password1) < 7:
            print("e")
            flash('Password must be at least 7 chars',category='error')
        else:
            new_user = User(email=email,first_name=first_name,password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user,remember=True)
            return redirect(url_for('views.home'))

    return render_template('sign_up.html',user=current_user)

