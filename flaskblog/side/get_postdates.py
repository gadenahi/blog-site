"""
This module is to get post data by year and month
"""
from flaskblog.models import Post
from collections import defaultdict


def get_postdates():
    """
    To get the data by year and month to count the total number
    :return: dictionary by year and month
    """
    posts = Post.query.all()
    year_dict = defaultdict(int)
    month_dict = defaultdict(int)
    for post in posts:
        year_dict[str(post.date_posted.year)] += 1
        month_dict[str(post.date_posted.year)+"-"+str(post.date_posted.month)]\
            += 1

    # print(year_dict)
    # for k, v in month_dict.items():
    #     print(k, v)
    # year_dict = {
    #     '2019': 20,
    #     '2018': 19
    # }
    # month_dict = {
    #     '2019-12': 12,
    #     '2019-11': 11,
    #     '2019-10': 10,
    #     '2019-9': 9,
    #     '2019-8': 8,
    #     '2019-7': 7,
    #     '2019-6': 6,
    #     '2019-5': 5,
    #     '2019-4': 4,
    #     '2019-3': 3,
    #     '2019-2': 2,
    #     '2019-1': 1,
    #     '2018-12': 12,
    #     '2018-11': 11,
    #     '2018-10': 10,
    #     '2018-9': 9,
    #     '2018-8': 8,
    #     '2018-7': 7,
    #     '2018-6': 6,
    #     '2018-5': 5,
    #     '2018-4': 4,
    #     '2018-3': 3,
    #     '2018-2': 2,
    #     '2018-1': 1,
    # }

    return year_dict, month_dict
