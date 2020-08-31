"""
This module is models for User and Post
"""
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flaskblog import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def loader_user(user_id):
    """
    To get the user information when login in.
    :param user_id: login user id
    :return: login user id
    """
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """
    User models for user information
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        """
        To generate the token with secret_key
        :param expires_sec: expire time for token. second
        :return: token
        """
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        """
        To verify if the user is in the database with the token
        :param token: token is provided by get_reset_token()
        :return: user information
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        # except:
        finally:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        """
        for the debug purpose by shell script
        :return:username, email and image_file
        """
        return "User('{}', '{}', '{}')".format(self.username, self.email,
                                               self.image_file)


class Post(db.Model):
    """
    Post models for post information for blog site.
    user_id has a relationship with user.id of user class as author
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        """
        for the debug purpose by shell script
        :return:tile, date_posted
        """
        return "Post('{}', '{}')".format(self.title, self.date_posted)


# def init():
#     db.create_all()
