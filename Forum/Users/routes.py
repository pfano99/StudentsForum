from flask import Blueprint, session, render_template, redirect, url_for, request, abort
from Forum.Users.forms import RegistrationForm, LoginForm, UpdateProfileForm
from Forum.models import User, Post
from Forum import db, bcrypt
from flask_login import login_user, logout_user, current_user, login_required
from Forum.Utility.utils import SaveDocuments, format_email
users = Blueprint('users', __name__)


@users.route('/register', methods = ['POST', 'GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            first_name = form.name.data,
            gender=form.gender.data,
            email = format_email(form.email.data),
            password = hashed_password 
        )
        db.session.add(user)
        db.session.commit()
        return  redirect(url_for('users.login'))
    return render_template('register.html', title = 'Registration', form = form)


@users.route('/login', methods = ['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session['account_type'] = 'Normal'
        user = User.query.filter_by(email = format_email(form.email.data)).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return  redirect(url_for('main.home'))
    return render_template('login.html', title = 'login', form = form)


@users.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('account_type', None)
    return redirect(url_for('main.index'))


@users.route('/account', methods = ['POST', 'GET'])
@login_required
def account():
    form = UpdateProfileForm()
    if request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me
        form.course.data = current_user.course
        form.school.data = current_user.school

    elif request.method == 'POST':    
        if form.validate_on_submit():
            if form.profile_picture.data:
                pic = SaveDocuments()
                current_user.profile_picture = pic.save_profile_picture(form.profile_picture.data)

            current_user.first_name = form.first_name.data
            current_user.last_name = form.last_name.data
            current_user.email = form.email.data
            current_user.about_me = form.about_me.data
            current_user.school = form.school.data
            current_user.course = form.course.data

            db.session.commit()
            return redirect(url_for('users.account'))

    return render_template('User/account.html', title = 'Account', form = form)


@users.route('/profile/<int:user_id>', methods = ['GET'])
@login_required
def user_profile(user_id):
    user = User.query.get_or_404(user_id)
    user_posts = Post.query.filter_by(user_id = user_id)
    return render_template('User/profile.html', user = user, posts = user_posts)



@users.route('/profile/follow/<int:user_id>')
@login_required
def follow(user_id):
    user = User.query.get(user_id)
    if user and user == current_user:
        return "You cannot follow yourself"

    elif user is None:
        return redirect(url_for('home'))
    
    current_user.follow(user)
    db.session.commit()
    return redirect(url_for('users.user_profile', user_id = user_id))



@users.route('/profile/unfollow/<int:user_id>')
@login_required
def unFollow(user_id):
    user = User.query.get(user_id)

    if user and user != current_user:
        current_user.unfollow(user)
        db.session.commit()
        return redirect(url_for('users.user_profile', user_id = user_id))
    
    elif user == current_user:
        return "You cannot unfollow yourself"
    else:
        return "user not found"

