"""
This module is setting for SQL server and mail server
"""

import os


class Config:
    """
    Setting for SQL and mail server
    """
    # move to  .bash_profile
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or \
                              os.environ.get('DATABASE_URL')
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    # MAIL_USERNAME = os.environ.get('EMAIL_USER') # use your own account
    # MAIL_PASSWORD = os.environ.get('EMAIL_PASS') # use your own account
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # https://stackoverflow.com/questions/28209414/sending-a-mail-from-flask-mail-smtpsenderrefused-530
