"""
This module is route and def for posts
"""
from flask import (render_template, url_for, flash, redirect,
                   request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post
from flaskblog.posts.forms import PostForm
from flaskblog.side.get_postdates import get_postdates


posts = Blueprint('posts', __name__)


@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    """
    To post the new blogs on the website
    :return: render create_post.html, title, form, legend, year_dict,
    month_dict, side_posts
    """
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    # to get the number of posts by year and month for submenu
    year_dict, month_dict = get_postdates()
    side_posts = Post.query.order_by(Post.date_posted.desc()).limit(5)
    return render_template('create_post.html', title='New Post', form=form,
                           legend='New Post', year_dict=year_dict,
                           month_dict=month_dict, side_posts=side_posts)


@posts.route('/post/<int:post_id>')
def post(post_id):
    """
    To show the each posts
    :param post_id: unique number by post
    :return: render post.html, title, post, year_dict, month_dict, side_posts
    """
    post = Post.query.get_or_404(post_id)
    year_dict, month_dict = get_postdates()
    side_posts = Post.query.order_by(Post.date_posted.desc()).limit(5)
    return render_template('post.html', title=post.title, post=post,
                           year_dict=year_dict, month_dict=month_dict,
                           side_posts=side_posts)


@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    """
    To update the post
    :param post_id: unique number by post
    :return: if update post submitted, redirect posts.post and post.id.
    Render the create_post.html, title, from, legend, year_dict, month_dict,
    side_posts
    """
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    # if update post is submitted, redirected to posts.post
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    # To get the title and content to show it on the form
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    year_dict, month_dict = get_postdates()
    side_posts = Post.query.order_by(Post.date_posted.desc()).limit(5)
    return render_template('create_post.html', title='Update Post', form=form,
                           legend='Update Post', year_dict=year_dict,
                           month_dict=month_dict, side_posts=side_posts)


@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    """
    To delete post by post_id
    :param post_id: unique id by post
    :return: redirect to homepage
    """
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))
