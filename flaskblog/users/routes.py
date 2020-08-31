"""
This module is route and def for users
"""
from flask import (render_template, url_for, flash, redirect, request,
                   Blueprint)
from flaskblog import db, bcrypt
from flaskblog.users.forms import (RegistrationForm, LoginForm,
                                   UpdateAccountForm, RequestResetForm,
                                   ResetPasswordForm, UpdatePasswordForm)
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog.users.utils import save_picture, send_reset_email
from flaskblog.side.get_postdates import get_postdates


"""
As of Apr. 3, 2020, need to use werkzeug==0.16.0 due to the degrade of 1.0.0
"""

users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    """
    To register the account for new users
    :return: if authenticated, redirect to homepage.
    if registration is submitted, redirect to login page
    At default, render registration page, title, form, year_dict, month_dict,
    side_posts
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.
                                                        data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data,
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('users.login'))
    year_dict, month_dict = get_postdates()
    side_posts = Post.query.order_by(Post.date_posted.desc()).limit(5)
    return render_template('register.html', title='Register', form=form,
                           year_dict=year_dict, month_dict=month_dict,
                           side_posts=side_posts)


@users.route('/login', methods=['GET', 'POST'])
def login():
    """
    To login
    :return: if authenticated, redirected to homepage
    if login form is submitted, and url contains next, redirect to next page,
    otherwise to homepage
    At default render login.html, title, form, year_dict, month_dict,
    side_posts
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # to check the password
        if user and bcrypt.check_password_hash(user.password,
                                               form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('You have been logged in!', 'success')
            return redirect(next_page) if next_page else redirect(
                url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check username and password',
                  'danger')
    year_dict, month_dict = get_postdates()
    side_posts = Post.query.order_by(Post.date_posted.desc()).limit(5)
    return render_template('login.html', title='Login', form=form,
                           year_dict=year_dict, month_dict=month_dict,
                           side_posts=side_posts)


@users.route('/logout')
def logout():
    """
    To logout
    :return: redirect to homepage
    """
    logout_user()
    return redirect(url_for('main.home'))


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    """
    To update the account information
    :return: if the form is submitted, redirect to users.account, else
    render account.html, title, image_file, form, year_dict, month_dict,
    side_posts with the current user and email filled on the form
    """
    form = UpdateAccountForm()
    if form.validate_on_submit():
        # if the picture is updated
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    # to show the image data on the web site
    image_file = url_for('static',
                         filename='profile_pics/' + current_user.image_file)
    year_dict, month_dict = get_postdates()
    side_posts = Post.query.order_by(Post.date_posted.desc()).limit(5)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form,
                           year_dict=year_dict, month_dict=month_dict,
                           side_posts=side_posts)


@users.route('/user/<string:username>')
def user_posts(username):
    """
    To show the posts by username
    :param username: username registered on the db
    :return: render user_posts.html, posts, user, year_dict, month_dict,
    side_posts
    """
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    year_dict, month_dict = get_postdates()
    side_posts = Post.query.order_by(Post.date_posted.desc()).limit(5)
    return render_template('user_posts.html', posts=posts, user=user,
                           year_dict=year_dict, month_dict=month_dict,
                           side_posts=side_posts)


@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    """
    TO send the email to reset password
    :return: if authenticated, redirect to homepage
    if form is submitted, redirect to user login
    At default, render reset_request.html, title, form
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # send email
        send_reset_email(user)
        flash('An email has been sent with instructions to reset'
              'your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html',
                           title='Reset Password', form=form)


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    """
    To reset the password with token provided by email
    :param token: token generated by get_reset_token and provided by email
    :return: If authenticated, redirect to homepage
    if user is None, redirect to reset_request,
    if form is submitted, redirect to login page
    At default, render reset_token.html, with title and form
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid token or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data). \
                          decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been update! You are now able to log in',
              'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html',
                           title='Reset Password', form=form)


@users.route('/account/<string:username>/update_password',
             methods=['GET', 'POST'])
def update_password(username):
    """
    To update the password with authenticated user
    :param username: current login user
    :return: if form is submitted, redirect to users.account
    At default, render update_password.html, title, image_file, form, year_dict
    , month_dict, side_posts
    """
    form = UpdatePasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password,
                                               form.oldpassword.data):
            hashed_password = bcrypt.generate_password_hash(
                form.password.data).decode('utf-8')
            current_user.password = hashed_password
            db.session.commit()
            flash('Your password has been updated!', 'success')
            return redirect(url_for('users.account'))
    image_file = url_for('static',
                         filename='profile_pics/' + current_user.image_file)
    year_dict, month_dict = get_postdates()
    side_posts = Post.query.order_by(Post.date_posted.desc()).limit(5)
    return render_template('update_password.html', title='Update Password',
                           image_file=image_file, form=form,
                           year_dict=year_dict, month_dict=month_dict,
                           side_posts=side_posts)
