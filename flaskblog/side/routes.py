"""
This module is routes and def for posts by year and month
"""
import calendar
from datetime import datetime
from flask import render_template, request, Blueprint
from flaskblog.models import Post
from flaskblog.side.get_postdates import get_postdates
import re

side = Blueprint('side', __name__)


@side.route('/archive/<string:filter_date>')
def date_posts(filter_date, start_month=1, end_month=12):
    """
    To show the posts by year and month
    :param filter_date: Input date of year or month to filter
    :param start_month: start_month to filter
    :param end_month: end_month to filter
    :return: render archive.html, posts, year, year_dict, month_dict,
    side_posts
    """
    page = request.args.get('page', 1, type=int)
    # To check if the filter_date is only year
    pattern = r"^\d{4}$"
    # To extract the year for the filter_date with year and month
    pattern_y = r"^\d{4}"
    # To extract the month for the filter_date with year and month
    pattern_m = r"(\d{4})-(\d{1,2})"
    re_pattern = re.compile(pattern)
    re_pattern_y = re.compile(pattern_y)
    re_pattern_m = re.compile(pattern_m)
    if re_pattern.match(filter_date):
        year = filter_date
    else:
        year = re_pattern_y.match(filter_date).group(0)
        start_month = re_pattern_m.match(filter_date).group(2)
        # to filter the month
        end_month = start_month
    # To set the start date for the filter
    start = datetime(year=int(year), month=int(start_month), day=1)
    # To get the last date by month automatically
    last_day = calendar.monthrange(int(year), int(start_month))[1]
    # To set the end date for the filter
    end = datetime(year=int(year), month=int(end_month), day=int(last_day))
    posts = Post.query.filter(Post.date_posted <= end)\
        .filter(Post.date_posted >= start)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    year_dict, month_dict = get_postdates()
    # if month filter, need to return year and month with year parameter
    if not re_pattern.match(filter_date):
        year = year + "-" + start_month
    side_posts = Post.query.order_by(Post.date_posted.desc()).limit(5)
    return render_template('archive.html', posts=posts, year=year,
                           year_dict=year_dict, month_dict=month_dict,
                           side_posts=side_posts)


"""
from datetime import datetime

start = datetime(year=2016,month=11,day=1)
end = datetime(year=2016,month=11,day=30)

posts = Post.query.filter(Post.date_posted <= end).filter(Post.date_posted 
>= start).all()
"""
