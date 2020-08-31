"""
This module is routes and def for homepage and about
"""
from flask import render_template, request, Blueprint
from flaskblog.models import Post
from flaskblog.side.get_postdates import get_postdates

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    """
    To show teh posts on the homepage
    :return: render home.html, posts, year_dict, month_dict, side_posts
    """
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page,
                                                                  per_page=5)
    year_dict, month_dict = get_postdates()
    side_posts = Post.query.order_by(Post.date_posted.desc()).limit(5)
    return render_template('home.html', posts=posts, year_dict=year_dict,
                           month_dict=month_dict, side_posts=side_posts)


@main.route('/about')
def about():
    """
    To show about of blog site
    :return: render about.html, title, year_dict, month_dict, side_posts
    """
    year_dict, month_dict = get_postdates()
    side_posts = Post.query.order_by(Post.date_posted.desc()).limit(5)
    return render_template('about.html', title='About', year_dict=year_dict,
                           month_dict=month_dict, side_posts=side_posts)
